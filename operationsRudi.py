
import SyntaxRUDI
import re
from _collections import deque

operatorPrecedence = {'*':1,'/':1,'+':2,'-':2}

class PrimitiveType():
    def evaluate(self):
        return self.val

    def getType(self):
        return self.type

class ControlSection():
    pass

class IOSection():
    pass

class variableExpr(PrimitiveType):
    def __init__ (self, val, type):
        self.val = val
        self.type = type

class integerExpr(PrimitiveType):
    def __init__ (self, val, type):
        self.val = val
        self.type = type

class floatExpr(PrimitiveType):
    def __init__ (self, val, type):
        self.val = val
        self.type = type

class stringExpr(PrimitiveType):
    def __init__ (self, val, type):
        self.val = val
        self.type = type

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
    def __init__ (self, condition, trueSection, falseSection):
        self.condition = condition
        self.trueSection = trueSection
        self.falseSection = falseSection

    def __str__(self):
        return 'If (%s) then [ %s ] else [%s]' % (self.condition, self.trueSection, self.falseSection)

    def evaluate(self, localVars):
        return ""

class whileSection(ControlSection):
    def __init__ (self, condition, trueSection):
        self.condition = condition
        self.trueSection = trueSection

    def __str__(self):
        return 'while (%s) [ %s ]' % (self.condition, self.trueSection)

    def evaluate(self, localVariables):
        resultOfCondition = self.condition.evaluate(localVariables)
        while (resultOfCondition):
            self.trueSection.evaluate(localVariables)
            resultOfCondition = self.condition.evaluate(localVariables)

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
                localVars[self.left] = tokenEvaluation(self.lineNum, tokensFromRight[0], localVars)
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

def tokenEvaluation(lineNum, t, localVariables):
    if t[1] == 'variable':
        if t[0] in localVariables:
            return localVariables[t[0]]
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

def postfixEvaluator(postfixOutput, localVars):
    operandStack = []
    for val in postfixOutput:
        if val[0] in operatorPrecedence:
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
            operandStack.append(tempResult)
        else:
            if val[1] == 'variable':
                processedValue = localVars.get(val[0])[1]
            else:
                processedValue = val[0]
            operandStack.append(processedValue)
    return operandStack.pop()