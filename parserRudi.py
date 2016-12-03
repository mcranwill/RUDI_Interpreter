import SyntaxRUDI
import _collections

def parserRudi():
    # Start Parsing
    print("Hello from parser!")


#   Assumptions:
#       There is one statement per line
def parseToLineList(listOfProgramLines):
    executableLines = []
    errorMessages = []
    flag_MultiLineComment = False

    #   First we remove all comment text from each line
    for line in listOfProgramLines:
        #   Handle making everything lowercase and perform strip
        line = makeLowerStrip(line)

        #   Make all of line lower case since syntax is case-insensitive per project description
        if not flag_MultiLineComment:
            #   Check if the line contains a comment and has both opening and closing comment tags
            if line.find('/*') > -1 and line.find('*/') > -1:
                lineNoComment = line.partition('/*')[0].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
            #   We have found that a multiline comment is being used
            elif line.find('/*') > -1:
                lineNoComment = line.partition('/*')[0].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
                flag_MultiLineComment = True
            else:
                if line != '':
                    executableLines.append(line)
        else:
            #   Check if we have found the closing symbol for a multiline comment
            if line.find('*/') > -1:
                #   Now we want the index of 2 since we want after the partition symbol
                lineNoComment = line.partition('*/')[2].strip()
                if lineNoComment != '':
                    executableLines.append(lineNoComment)
                #   Remember to set the flag to false
                flag_MultiLineComment = False

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


if __name__ == '__main__':
    parserRudi()