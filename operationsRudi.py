#   Collection of operations that implement functionality of controls
#   and expressions.  Implements the conversion from infix to postfix
#   notation using the Shunting-Yard Algorithm that is applied to both
#   arithmetic and boolean expressions.
#
#   RUDI Interpreter Final Project- Fall 2016
#   Data Structures & Algorithms for Practicing Engineers
#   Prof. Manuel Rosso-Llopart, Carnegie-Mellon University
#   Authors: Michael Cranwill & Erik Sjoberg

import SyntaxRUDI
import re
from ResourceTypes import *

operatorPrecedence = {'*':1,'/':1,'+':2,'-':2,':eq:':2,':ne:':2,':gt:':2,':lt:':2,':le:':2,':ge:':2,'^':4,'|':4,'~':4}
conditionalOperators = {':eq:':2,':ne:':2,':gt:':2,':lt:':2,':le:':2,':ge:':2,'^':4,'|':4,'~':4}

##  Classes that handle processing of each type of statement

class ControlSection():
    pass

class IOSection():
    def __init__(self):
        pass

    def evaluate(self, ioLine, localVars, lineNum):
        if ioLine[1].find('print') > -1:
            before, part, temp_arr = ioLine[1].partition('"')
            if temp_arr == '':
                temp_arr = ioLine[1].split(' ')[1]
            if str(temp_arr).find('"') > -1:
                print(temp_arr.replace('"', ''), end="")
            elif temp_arr == 'cr':
                print("")
            elif not temp_arr in localVars:
                print(SyntaxRUDI.InvalidVariable(ioLine[0], temp_arr))
            else:
                print(str(localVars.get(temp_arr)[1]), end="")
        elif ioLine[1].find('input') > -1:
            temp_arr = ioLine[1].split(' ')
            if not temp_arr[1] in localVars:
                print(SyntaxRUDI.InvalidVariable(ioLine[0], temp_arr[1]))
            else:
                localVars[temp_arr[1]] = (localVars.get(temp_arr[1])[0], getInput(localVars.get(temp_arr[1])[0]))

class printRudi(IOSection):
    pass

class getInputRudi(IOSection):
    pass

class arithmeticSection():
    def __init__(self, tokens):
        self.tokens = tokens

    def evaluate(self, localVars):
        operators = []
        postfixOutput = []
        for t in self.tokens:
            if t[1] == 'operator':
                if (checkPrecedence(operators, t[0])):
                    operators.append(t)
                else:
                    if t[0] == ')':
                        while operators[-1][0] != '(':
                            postfixOutput.append(operators.pop())
                        operators.pop()
                    else:
                        postfixOutput.append(operators.pop())
                        operators.append(t)
            else:
                postfixOutput.append(t)
        while len(operators)> 0:
            postfixOutput.append(operators.pop())

        return postfixEvaluator(postfixOutput, localVars)

class ifSection(ControlSection):
    def __init__ (self, condition, trueSection, falseSection, lineNum):
        temp_condition = re.match('if \([<A-Z><a-z><0-9>.\(\)\:\^\|\~ ]+\)', condition)
        condition = temp_condition.group(0).replace('if', '').replace('(', '').replace(')', '').strip()
        if len(condition) > 0:
            temp_arr = condition.split()
            self.condition = temp_arr
        else:
            return SyntaxRUDI.IfConditionInvalid(lineNum)
        self.trueSection = trueSection
        self.falseSection = falseSection
        self.lineNum = lineNum

    def __str__(self):
        return 'If (%s) then [ %s ] else [%s]' % (self.condition, self.trueSection, self.falseSection)

    def evaluate(self, localVars):
        tokens = []
        for r in self.condition:
            tokens.append(whatTypeAmI(r))
        operators = []
        postfixOutput = []
        for t in tokens:
            if t[1] == 'operator':
                if (checkPrecedence(operators, t[0])):
                    operators.append(t)
                else:
                    if t[0] == ')':
                        while operators[-1][0] != '(':
                            postfixOutput.append(operators.pop())
                        operators.pop()
                    else:
                        postfixOutput.append(operators.pop())
                        operators.append(t)
            else:
                postfixOutput.append(t)
        while len(operators) > 0:
            postfixOutput.append(operators.pop())

        boolValue = postfixEvaluator(postfixOutput, localVars)
        if boolValue:
            for line in self.trueSection:
                ExprToEvaluate(line, line[0], localVars)
        else:
            if self.falseSection != None:
                for line in self.falseSection:
                    ExprToEvaluate(line, line[0], localVars)

class whileSection(ControlSection):
    def __init__ (self, condition, trueSection, lineNum):
        temp_condition = re.match('while \([<A-Z><a-z><0-9>.\(\)\:\^\|\~ ]+\)', condition)
        condition = temp_condition.group(0).replace('while', '').replace('(', '').replace(')', '').strip()
        if len(condition) > 0:
            temp_arr = condition.split()
            self.condition = temp_arr
        else:
            return SyntaxRUDI.WhileConditionInvalid(lineNum)
        self.trueSection = trueSection
        self.lineNum = lineNum

    # def __init__ (self, condition, trueSection):
    #     self.condition = condition
    #     self.trueSection = trueSection

    def __str__(self):
        return 'while (%s) [ %s ]' % (self.condition, self.trueSection)

    def evaluate(self, localVars):
        tokens = []
        for r in self.condition:
            tokens.append(whatTypeAmI(r))
        operators = []
        postfixOutput = []
        for t in tokens:
            if t[1] == 'operator':
                if (checkPrecedence(operators, t[0])):
                    operators.append(t)
                else:
                    if t[0] == ')':
                        while operators[-1][0] != '(':
                            postfixOutput.append(operators.pop())
                        operators.pop()
                    else:
                        postfixOutput.append(operators.pop())
                        operators.append(t)
            else:
                postfixOutput.append(t)
        while len(operators) > 0:

            postfixOutput.append(operators.pop())

        boolValue = postfixEvaluator(postfixOutput, localVars)

        #resultOfCondition = self.condition.evaluate(localVariables)
        while (boolValue):
            for line in self.trueSection:
                ExprToEvaluate(line, line[0], localVars)
            boolValue = postfixEvaluator(postfixOutput, localVars)
            #resultOfCondition = self.condition.evaluate(localVariables)

class assignLine():
    def __init__(self, left, operator, right, lineNum):
        self.lineNum = lineNum
        if operator != '=':
            return SyntaxRUDI.InvalidAssignmentNoOperator(lineNum)
        self.operator = operator
        self.left = left
        if len(right) == 0:
            return SyntaxRUDI.InvalidAssignmentEmptyOperand(lineNum)
        self.right = right

    def __str__(self):
        return '%s = %s' % (self.left, self.right)

    def evaluate(self, localVars):
        #   Does the variable to be updated even exist
        if self.left in localVars:
            #   Check if only one element
            tokensFromRight = []
            for r in self.right:
                tokensFromRight.append(whatTypeAmI(r))
            if len(tokensFromRight) == 1:
                localVars[self.left] = (localVars[self.left][0], tokenEvaluation(self.lineNum, tokensFromRight[0], localVars))
            else:
                arithSection = arithmeticSection(tokensFromRight)
                if localVars[self.left][0] == 'integer':
                    localVars[self.left] = ('integer', int(arithSection.evaluate(localVars)))
                elif localVars[self.left][0] == 'float':
                    localVars[self.left] = ('float', float(arithSection.evaluate(localVars)))
                else:
                    return SyntaxRUDI.InvalidArithmeticType(self.lineNum)
        else:
            return SyntaxRUDI.InvalidVariable(self.lineNum, self.left)


##  Helper Functions
def tokenEvaluation(lineNum, t, localVariables):
    if t[1] == 'variable':
        if t[0] in localVariables:
            return localVariables[t[0]][1]
        else:
            print("ERROR: " + SyntaxRUDI.InvalidVariable(lineNum, t[0]))
            exit(1)
    elif  t[1] == 'string':
        return t[0]
    elif t[1] == 'float':
        return t[0]
    elif t[1] == 'integer':
        return t[0]

def whatTypeAmI(seeker):
    if seeker.find('"') > -1:
        return (seeker, 'string')
    if seeker == '0':
        return (0, 'integer')
    try:
        tempVar = int(seeker)
    except ValueError:
        tempVar = False
    if tempVar:
        return (tempVar,'integer')
    try:
        tempVar = float(seeker)
    except ValueError:
        tempVar = False
    if tempVar:
        return (tempVar, 'float')

    if seeker in conditionalOperators:
        return (seeker,'operator')

    #   Maybe I am an operator
    m = re.match('[\+\-\*\/\=\(\)]+', seeker)
    if m:
        return (seeker,'operator')

    else:
        return (seeker,'variable')

def checkPrecedence(operators,new_operator):
    if len(operators) == 0:
        return True
    if new_operator == '(':
        return True
    if new_operator == ')':
        return False
    currentOperPrecedence = operatorPrecedence.get(operators[-1][0])
    newOperPrecedence = operatorPrecedence.get(new_operator)
    if (newOperPrecedence < currentOperPrecedence):
        return True
    else:
        return False

def ExprToEvaluate(lineOrControl,lineNum, localVars):
    if lineOrControl[2] == SectionType.arithmetic_operation:
            temp_arr = str(lineOrControl[1]).split(' ')
            al = assignLine(temp_arr[0].strip(), temp_arr[1].strip(), temp_arr[2:],
                            lineOrControl[0])
            al.evaluate(localVars)
    elif lineOrControl[2] == SectionType.while_control:
        wc = whileSection(lineOrControl[1],lineOrControl[3],lineNum)
        wc.evaluate(localVars)
    elif lineOrControl[2] == SectionType.if_control:
        condition = lineOrControl[1]
        trueSection = lineOrControl[3]
        if len(lineOrControl) == 5:
            falseSection = lineOrControl[4]
        else:
            falseSection = None
        ifElem = ifSection(condition, trueSection, falseSection, lineNum)
        ifElem.evaluate(localVars)
    elif lineOrControl[2] == SectionType.io_operation:
        isection = IOSection()
        isection.evaluate(lineOrControl,localVars,lineOrControl[0])
        #wc.evaluate(localVars)

def postfixEvaluator(postfixOutput, localVars):
    operandStack = []
    for val in postfixOutput:
        if val[0] in operatorPrecedence or val[0] in conditionalOperators:
            if val[0] == '~':
                operandTwo = operandStack.pop()
                tempResult = not operandTwo
            else:
                operandTwo = operandStack.pop()
                operandOne = operandStack.pop()
            if val[0] == '*':
                tempResult = operandOne * operandTwo
            elif val[0] == '/':
                tempResult = operandOne / operandTwo
            elif val[0] == '+':
                tempResult = operandOne + operandTwo
            elif val[0] == '-':
                tempResult = operandOne - operandTwo
            elif val[0] == ':eq:':
                tempResult = operandOne == operandTwo
            elif val[0] == ':ne:':
                tempResult = operandOne != operandTwo
            elif val[0] == ':gt:':
                tempResult = operandOne > operandTwo
            elif val[0] == ':lt:':
                tempResult = operandOne < operandTwo
            elif val[0] == ':ge:':
                tempResult = operandOne >= operandTwo
            elif val[0] == ':le:':
                tempResult = operandOne <= operandTwo
            elif val[0] == '^':
                tempResult = operandOne and operandTwo
            elif val[0] == '|':
                tempResult = operandOne or operandTwo
            # elif val[0] == '~':
            #     tempResult = operandOne <= operandTwo
            operandStack.append(tempResult)
        else:
            if val[1] == 'variable':
                processedValue = localVars.get(val[0])[1]
            else:
                processedValue = val[0]
            operandStack.append(processedValue)
    return operandStack.pop()

def getInput(type):
    first = True
    while True:
        if type == 'string':
            try:
                if first:
                    userInput = input()
                    first = False
                else:
                    userInput = input("Enter a " + type)
            except ValueError:
                print("That's not a string")
                continue
            else:
                print("You entered " + userInput)
                break
        elif type == 'float':
            try:
                if first:
                    userInput = float(input())
                    first = False
                else:
                    userInput = float(input("Enter a " + type))
            except ValueError:
                print("That's not an integer")
                continue
            else:
                print("You entered " + str(userInput))
                break
        elif type == 'integer':
            try:
                if first:
                    userInput = int(input())
                    first = False
                else:
                    userInput = int(input("Enter a " + type))
            except ValueError:
                print("That's not an integer")
                continue
            else:
                print("You entered " + str(userInput))
                break
    return userInput