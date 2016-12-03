
def parserRudi():
    # Start Parsing
    print("Hello from parser!")

def parseToExecutionList(listOfProgramLines):
    executableLines = []
    errorMessages = []

    #   First we remove all comment text from each line
    for line in listOfProgramLines:
        #   Check if the line contains a comment
        if line.find('/*') > -1:
            lineNoComment = line.partition('/*')[0].strip()
            if lineNoComment != '':
                executableLines.append(lineNoComment)
        else:
            executableLines.append(line.strip())

    #   Next we validate specific elements to ensure consistency with syntax
    if str(executableLines[0]).lower().find('program') == -1:
        errorMessages.append("Line 1: Keyword 'program' should appear in this line")
    if str(executableLines[-1]).lower().find('end') == -1:
        errorMessages.append("Line "+ str(len(executableLines)) + ": Keyword 'end' should appear in this line")

    if len(errorMessages) > 0:
        return ["Error Messages"] + errorMessages
    else:
        return executableLines

def stripComment(lineWithComment):
    return lineWithComment.partition('/*')[0].strip()

if __name__ == '__main__':
    parserRudi()