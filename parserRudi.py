import SyntaxRUDI
import _collections
import ResourceTypes

def parserRudi():
    # Start Parsing
    print("Hello from parser!")

def validateSyntax(executionList):
    errorMessages = []
    executableSections = []

    #   Validate specific elements to ensure consistency with syntax
    if str(executionList[0]).lower().find('program') == -1:
        errorMessages.append(SyntaxRUDI.ERRORProgramMissing)

    if str(executionList[-1]).lower().find('end') == -1:
        errorMessages.append(SyntaxRUDI.ERROREndStatementMissing(len(executionList)))

    finishedDecs = False
    settingBegin = False
    i = 0

    while (i < len(executionList)-1):
        temp_str_val = str(executionList[i])
        if temp_str_val.find('decs') > -1:
            #   Now we need to find where decs ends and process until we get there
            #   First option is they are on the same line
            if finishedDecs == True:
                errorMessages.append(SyntaxRUDI.ERRORdecsDeclaredAlready(i))
            else:
                endIndexOfThisBracket = findCorrespondingEndBracketIndex(executionList[i:], i)
                if temp_str_val.find('[') > -1:
                    print("they are on the same line")
                elif str(executionList[i+1]).find('[') > -1:
                    print("it is one the next line")
                else:
                    errorMessages.append(SyntaxRUDI.ERRORdecsOpenBracketMissing(i))
                while i < endIndexOfThisBracket:
                    if executionList[i].find('integer') > -1 or \
                        executionList[i].find('float') > -1 or \
                        executionList[i].find('string') > -1:
                        executableSections.append((i,executionList[i],ResourceTypes.SectionType.declare_var))
                    i = i+1
                i = i-1
        elif temp_str_val.find('begin') > -1:
            settingBegin = True
        elif temp_str_val.find('while') > -1:
            if settingBegin == False:
                errorMessages.append(SyntaxRUDI.ERRORBeginStatementMissing(i))
            else:
                endIndexOfThisBracket = findCorrespondingEndBracketIndex(executionList[i:], i)
                associatedElems = createListForControl(executionList[i:endIndexOfThisBracket], i)
                tupleOfWhile = (i,temp_str_val,ResourceTypes.SectionType.while_control, associatedElems)
                executableSections.append(tupleOfWhile )
                i = endIndexOfThisBracket -1
        elif temp_str_val.find('if') > -1:
            if settingBegin == False:
                errorMessages.append(SyntaxRUDI.ERRORBeginStatementMissing(i))
            else:
                endIndexOfThisBracket = findCorrespondingEndBracketIndex(executionList[i:], i)
                associatedElems = createListForControl(executionList[i:endIndexOfThisBracket], i)
                tupleOfIf = (i, temp_str_val, ResourceTypes.SectionType.if_control, associatedElems)
                executableSections.append(tupleOfIf)

                i = endIndexOfThisBracket -1
        elif temp_str_val.find('else') > -1:
            if settingBegin == False:
                errorMessages.append(SyntaxRUDI.ERRORBeginStatementMissing(i))
            else:
                endIndexOfThisBracket = findCorrespondingEndBracketIndex(executionList[i:], i)
                associatedElems = createListForControl(executionList[i:endIndexOfThisBracket], i)
                tupleOfIf = (i, temp_str_val, ResourceTypes.SectionType.else_control, associatedElems)
                executableSections.append(tupleOfIf)
                i = endIndexOfThisBracket -1
        elif temp_str_val.find('print') > -1:
            subControlledTuple = (i , temp_str_val, ResourceTypes.SectionType.io_operation)
            executableSections.append(subControlledTuple)
        elif '+' in temp_str_val or '-' in temp_str_val or '*' in temp_str_val or \
                '/' in temp_str_val or '=' in temp_str_val:
            subControlledTuple = (i , temp_str_val, ResourceTypes.SectionType.arithmetic_operation)
            executableSections.append(subControlledTuple)
        i = i + 1

    if len(errorMessages) > 0:
        return ["Error Messages"] + errorMessages
    else:
        return executableSections


#   Assumptions:
#       There is one statement per line
def parseToLineList(listOfProgramLines):
    executableLines = []
    errorMessages = []
    flag_MultiLineComment = False

    #   First we remove all comment text from each line
    i = 0
    while i < len(listOfProgramLines):
        #   Handle making everything lowercase and perform strip
        line = makeLowerStrip(listOfProgramLines[i])

        if line.find('&') > -1:
            if str(listOfProgramLines[i+1]).find('&') > -1:
                newLine = line.replace('&', '') + \
                          makeLowerStrip(str(listOfProgramLines[i + 1])).replace('&', '') + \
                          makeLowerStrip(str(listOfProgramLines[i + 2])).replace('&', '')
                i = i + 2
            else:
                newLine = line.replace('&', '') + " " + \
                          makeLowerStrip(str(listOfProgramLines[i + 1]))
                i = i + 1
        else:
            newLine = line

        #   Make all of line lower case since syntax is case-insensitive per project description
        if not flag_MultiLineComment:
            #   Check if the line contains a comment and has both opening and closing comment tags
            if newLine.find('/*') > -1 and newLine.find('*/') > -1:
                lineNoComment = newLine.partition('/*')[0].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
            #   We have found that a multiline comment is being used
            elif newLine.find('/*') > -1:
                lineNoComment = newLine.partition('/*')[0].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
                flag_MultiLineComment = True
            else:
                if newLine != '':
                    executableLines.append(line)
        else:
            #   Check if we have found the closing symbol for a multiline comment
            if newLine.find('*/') > -1:
                #   Now we want the index of 2 since we want after the partition symbol
                lineNoComment = newLine.partition('*/')[2].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
                #   Remember to set the flag to false
                flag_MultiLineComment = False
        i = i + 1

    # #   Next we validate specific elements to ensure consistency with syntax
    # if str(executableLines[0]).lower().find('program') == -1:
    #     errorMessages.append(SyntaxRUDI.ERRORProgramMissing)
    # if str(executableLines[-1]).lower().find('end') == -1:
    #     errorMessages.append(SyntaxRUDI.ERROREndStatementMissing(len(executableLines)))
    #
    # numOpenBrackets = 0
    # d = _collections.deque()
    # listOfOpenBrackets = []
    # # for bracketedLine in executableLines:
    # #     if bracketedLine.find('(') > -1 or bracketedLine.find('[') > -1 or bracketedLine.find('{') > -1:
    # #         numOpenBrackets = numOpenBrackets + 1

    if len(errorMessages) > 0:
        for l in executableLines:
            print(l)
        return ["Error Messages"] + errorMessages
    else:
        return executableLines


def makeLowerStrip(line):
    if line.find('"') > -1:
        line = lowerExceptString(line.strip())
    else:
        line = line.lower().strip()

    return line


def stripComment(lineWithComment):
    return lineWithComment.partition('/*')[0].strip()

def lowerExceptString(line):
    newLine = ""
    if str(line).count('"') == 2:
        beforePart, part, afterPart = line.partition('"')
    else:
        print("Something very strange is happening")
        return newLine

    #   Ensure the last character of the line is "
    if afterPart[-1] == '"':
        newLine = beforePart.lower() + '"' + afterPart
    else:
        print("Something very strange is happening")
    return newLine


def createListForControl(listOfStrings, currentIndex):
    subExecutables = []
    i = 1
    while i < len(listOfStrings):
        temp_line = str(listOfStrings[i])
        #   Is there a sub element (while, if, else)?
        if temp_line.find('while') > -1:
            endIndexOfThisBracket = findCorrespondingEndBracketIndex(listOfStrings[i:], i+currentIndex)
            associated = createListForControl(listOfStrings[i:endIndexOfThisBracket], i+currentIndex)
            subControlledTuple = ( i+currentIndex, temp_line, ResourceTypes.SectionType.while_control, associated)
            subExecutables.append(subControlledTuple)
            i = endIndexOfThisBracket - 1
        elif temp_line.find('if') > -1:
            endIndexOfThisBracket = findCorrespondingEndBracketIndex(listOfStrings[i:], i+currentIndex)
            associated = createListForControl(listOfStrings[i:endIndexOfThisBracket], i + currentIndex)
            subControlledTuple = ( i+currentIndex, temp_line, ResourceTypes.SectionType.if_control, associated)
            subExecutables.append(subControlledTuple)
            i = endIndexOfThisBracket - 1
        elif temp_line.find('else') > -1:
            endIndexOfThisBracket = findCorrespondingEndBracketIndex(listOfStrings[i:], i+currentIndex)
            associated = createListForControl(listOfStrings[i:endIndexOfThisBracket], i + currentIndex)
            subControlledTuple = ( i+currentIndex, temp_line, ResourceTypes.SectionType.else_control, associated)
            subExecutables.append(subControlledTuple)
            i = endIndexOfThisBracket -1
        if temp_line.find('[') > -1:
            temp_line = temp_line.replace('[','').strip()
            if temp_line == '':
                i = i + 1
                continue
        elif temp_line.find(']') > -1:
            temp_line = temp_line.replace(']','').strip()
            if temp_line == '':
                i = i + 1
                continue
        if temp_line.find('print') > -1:
            subControlledTuple = (
                i + currentIndex, temp_line, ResourceTypes.SectionType.io_operation)
            subExecutables.append(subControlledTuple)
        elif '+' in temp_line or '-' in temp_line or '*' in temp_line or '/' in temp_line or '=' in temp_line:
            subControlledTuple = (
                i + currentIndex, temp_line, ResourceTypes.SectionType.arithmetic_operation)
            subExecutables.append(subControlledTuple)
        i = i + 1
    return subExecutables

def findCorrespondingEndBracketIndex(listOfStrings, currentIndex):
    #   Find the first index
    if listOfStrings[0].find('[') > -1:
        #   It's on the first line
        endIndexOfThisBracket = 1
    elif listOfStrings[1].find('[') > -1:
        #   It's actually on the second line
        endIndexOfThisBracket = 2
    else:
        return SyntaxRUDI.ERRORdecsOpenBracketMissing(currentIndex)

    numberOpenBrackets = 1
    while endIndexOfThisBracket < len(listOfStrings) and numberOpenBrackets > 0:
        if listOfStrings[endIndexOfThisBracket].find('[') > -1:
            numberOpenBrackets = numberOpenBrackets + 1
        if listOfStrings[endIndexOfThisBracket].find(']') > -1:
            numberOpenBrackets = numberOpenBrackets - 1
            if numberOpenBrackets == 0:
                break
            else:
                endIndexOfThisBracket = endIndexOfThisBracket + 1
        else:
            endIndexOfThisBracket = endIndexOfThisBracket + 1
    return endIndexOfThisBracket + currentIndex + 1

if __name__ == '__main__':
    parserRudi()