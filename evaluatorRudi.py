import SyntaxRUDI
import _collections
import ResourceTypes

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
                # if variableList.has_key(temp_arr):
                #
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
            temp_before, part, temp_after = str(executableSections[i][1]).partition('=')
            temp_before = temp_before.strip()
            temp_after = temp_after.strip()
            part = part.strip()
            if not temp_before in variableList:
                errorMessages.append(SyntaxRUDI.InvalidVariable(executableSections[i][0], temp_before))
            else:
                if temp_after.strip() in variableList:
                    newZerothTerm = variableList.get(temp_before.strip())[0]
                    newFirstTerm = variableList.get(temp_after.strip())[1]
                    variableList[temp_before] = (newZerothTerm,newFirstTerm)
                else:
                    #TODO: Make this actually work
                    print("Not Yet Implemented")
                    # temp_arr = temp_after.split(' ')
                    # if len(temp_arr) > 0:
                    #     #Non-basic assignment
                    #     variableList[temp_before] = evaluateExpression(temp_arr)
                    # elif not temp_after in variableList:
                    #     errorMessages.append(SyntaxRUDI.InvalidVariable(executableSections[i][0], temp_after))
                    # else:
                    #     variableList[temp_before] = variableList.get(temp_after)
        elif executableSections[i][2] == ResourceTypes.SectionType.if_control:
            print("")
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