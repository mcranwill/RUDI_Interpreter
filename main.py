import parserRudi
import evaluatorRudi


def main():
    rudiProgramLines = openFileForLines()

    executionList = parserRudi.parseToLineList(rudiProgramLines)
    executableSections = parserRudi.validateSyntax(executionList)

    evaluatorRudi.evaluatorRudi(executableSections)

    #   Do we have error messages to display?
    if type(executableSections[0]) != tuple:
        if str(executableSections[0]).find("Error Messages") > -1:
            for l in executableSections:
                print(l)
            exit()
    else:
        for l in executableSections:
            print(l)
    print("Everything parsed correctly.")

def openFileForLines():
    try:
        rudi_file = open("test.rudi", 'r')
        linesOfRudiProgram = rudi_file.readlines()
        rudi_file.close()
        return linesOfRudiProgram
    except FileNotFoundError:
        print("Oops the file was not found. " + str(FileNotFoundError.filename2))
        exit("File specified was not found")


if __name__ == '__main__':
    main()