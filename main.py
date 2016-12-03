import parserRudi

def main():
    rudiProgramLines = openFileForLines()

    executionList = parserRudi.parseToLineList(rudiProgramLines)

    print("Length of rudiProgramLines is " + str(len(rudiProgramLines)))
    print("Length of executionList is " + str(len(executionList)))

    #   Do we have error messages to display?
    if executionList[0].find("Error Messages") > -1:
        for l in executionList:
            print(l)
        exit()
    else:
        for l in executionList:
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