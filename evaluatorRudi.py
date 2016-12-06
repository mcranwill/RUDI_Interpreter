#   Evaluator processes each tuple and is a pass through to the
#   operations object that evaluates expressions and controls
#   defined within the operations object.
#
#   RUDI Interpreter Final Project- Fall 2016
#   Data Structures & Algorithms for Practicing Engineers
#   Prof. Manuel Rosso-Llopart, Carnegie-Mellon University
#   Authors: Michael Cranwill & Erik Sjoberg

import SyntaxRUDI
import ResourceTypes
from operationsRudi import *

def evaluatorRudi(executableSections):
    variableList = {}
    errorMessages = []

    i = 0

    while i < len(executableSections):
        if executableSections[i][2] == ResourceTypes.SectionType.declare_var:
            temp_arr = executableSections[i][1].split(' ')
            if temp_arr[0] == 'integer':
                variableList[temp_arr[1]] = ('integer',0)
            elif temp_arr[0] == 'string':
                variableList[temp_arr[1]] = ('string', '')
            elif temp_arr[0] == 'float':
                variableList[temp_arr[1]] = ('float', 0.0)
            else:
                errorMessages.append(SyntaxRUDI.InvalidType(executableSections[i][0], temp_arr[0]))
        else:
            ExprToEvaluate(executableSections[i], executableSections[i][0], variableList)
        i+=1

def printSubSections(t):
    print("line number is " + str(t[0]) + " statement: " + t[1] \
          + " and type is " + str(t[2]))
    for section in t[3]:
        if len(section) == 4:
            printSubSections(section)
        else:
            print("line number is " + str(section[0]) + " statement: " + section[1] \
                  + " and type is " + str(section[2]))


if __name__ == '__main__':
    evaluatorRudi()