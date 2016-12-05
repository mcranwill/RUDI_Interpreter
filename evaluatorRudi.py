import SyntaxRUDI
import _collections
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

    # for section in executableSections:
    #     if len(section) == 4:
    #         printSubSections(section)
    #     else:
    #         print("line number is " + str(section[0]) + " statement: " + section[1] \
    #               + " and type is " + str(section[2]))

def printSubSections(t):
    print("line number is " + str(t[0]) + " statement: " + t[1] \
          + " and type is " + str(t[2]))
    for section in t[3]:
        if len(section) == 4:
            printSubSections(section)
        else:
            print("line number is " + str(section[0]) + " statement: " + section[1] \
                  + " and type is " + str(section[2]))

def getInput(type):
    while True:

        if type == 'string':
            try:
                userInput = input("Enter a " + type)
            except ValueError:
                print("That's not a string")
                continue
            else:
                print("You entered " + userInput)
                break
        elif type == 'float':
            try:
                userInput = float(input("Enter a " + type))
            except ValueError:
                print("That's not an integer")
                continue
            else:
                print("You entered " + str(userInput))
                break
        elif type == 'integer':
            try:
                userInput = int(input("Enter a " + type))
            except ValueError:
                print("That's not an integer")
                continue
            else:
                print("You entered " + str(userInput))
                break
    return userInput

def evaluateExpression(temp_arr):
    i = 0
    while i < len(temp_arr):
        print(temp_arr[i])
        i+=1

if __name__ == '__main__':
    evaluatorRudi()