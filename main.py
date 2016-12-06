#   Driver program for RUDI Interpreter that reads in a file and
#   execute it per the RUDI grammar.  Program is written against
#   the Python3.5 language standard and is run like
#   python main.py <input_file> where input_file is like test.rudi
#
#   RUDI Interpreter Final Project- Fall 2016
#   Data Structures & Algorithms for Practicing Engineers
#   Prof. Manuel Rosso-Llopart, Carnegie-Mellon University
#   Authors: Michael Cranwill & Erik Sjoberg

import parserRudi
import evaluatorRudi
import sys

def main(args):
    if len(args)> 1:
        fileName = args[1]
    else:
        fileName = 'test.rudi'

    #   Collect all lines into a list for parsing
    rudiProgramLines = openFileForLines(fileName)

    #   Parse each line and handle if it ends in a & and remove all
    #   comments including multi-line
    executionList = parserRudi.parseToLineList(rudiProgramLines)

    #   For each parsed line discover its relationship to nearby lines
    #   by creating a tuple like
    #       (lineNumber, raw_line_text, enumType, <true_section>, <false_section>)
    #   true_section is mandatory for if_control and while_control
    #   false_section is optional for if_control
    executableSections = parserRudi.validateSyntax(executionList)

    #   Evaluator tokenizes operators and operands using the operationsRudi class
    #   to process the various controls and expressions
    evaluatorRudi.evaluatorRudi(executableSections)

    #   Do we have error messages to display, if so print them out.
    if type(executableSections[0]) != tuple:
        if str(executableSections[0]).find("Error Messages") > -1:
            for l in executableSections:
                print(l)
            exit()

#   Read all lines from file with name
#   @in:        filename to parse
#   @return:    a list of string lines or exit the program with error message
def openFileForLines(filename):
    try:
        rudi_file = open(filename, 'r')
        linesOfRudiProgram = rudi_file.readlines()
        rudi_file.close()
        return linesOfRudiProgram
    except FileNotFoundError:
        print("Oops the file was not found. " + str(FileNotFoundError.filename2))
        exit("File specified with name:" + filename + " was not found")


if __name__ == '__main__':
    main(sys.argv)