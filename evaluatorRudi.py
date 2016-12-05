import SyntaxRUDI
import _collections
import ResourceTypes
from operationsRudi import *

arithmetic_expressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),


]

def evaluatorRudi(executableSections):
    print("Hello from evaluatorRudi")
    executionStack = _collections.deque()
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
        elif executableSections[i][2] == ResourceTypes.SectionType.io_operation:
            if executableSections[i][1].find('print') > -1:
                before, part, temp_arr = executableSections[i][1].partition('"')
                if temp_arr == '':
                    temp_arr = executableSections[i][1].split(' ')[1]
                if str(temp_arr).find('"') > -1:
                    print(temp_arr.replace('"',''),end="")
                elif not temp_arr in variableList:
                    errorMessages.append(SyntaxRUDI.InvalidVariable(executableSections[i][0], temp_arr))
                else:
                    print(str(variableList.get(temp_arr)[1]),end="")
            elif executableSections[i][1].find('input') > -1:
                temp_arr = executableSections[i][1].split(' ')
                if not temp_arr[1] in variableList:
                    errorMessages.append(SyntaxRUDI.InvalidVariable(executableSections[i][0], temp_arr[1]))
                else:
                    variableList[temp_arr[1]] = (variableList.get(temp_arr[1])[0], getInput(variableList.get(temp_arr[1])[0]))
        elif executableSections[i][2] == ResourceTypes.SectionType.arithmetic_operation:
            temp_arr = str(executableSections[i][1]).split(' ')
            al = assignLine(temp_arr[0].strip(), temp_arr[1].strip(), temp_arr[2:], executableSections[i][0])
            al.evaluate(variableList)
        elif executableSections[i][2] == ResourceTypes.SectionType.if_control:
            condition = executableSections[i][1]
            trueSection = executableSections[i][3]
            if len(executableSections[i]) == 5:
                falseSection = executableSections[i][4]
            else:
                falseSection = None
            ifElem = ifSection(condition,trueSection,falseSection)
            ifElem.evaluate(variableList)
        elif executableSections[i][2] == ResourceTypes.SectionType.else_control:
            print("")
        elif executableSections[i][2] == ResourceTypes.SectionType.while_control:
            print("")
        i+=1

    for section in executableSections:
        if len(section) == 4:
            printSubSections(section)
        else:
            print("line number is " + str(section[0]) + " statement: " + section[1] \
                  + " and type is " + str(section[2]))

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