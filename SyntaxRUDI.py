#   Define all error strings that the application will need in one place.

ERRORProgramMissing = "Line 1: Keyword 'program' should appear in this line"
ERRORdecsMissing = "Line 2: Keyword 'decs' should appear in this line"
def ERRORdecsOpenBracketMissing(lineNum):
    return "Line "+ str(lineNum) + ": Open bracket should be on this line or the next"
def ERRORdecsDeclaredAlready(lineNum):
    return "Line "+ str(lineNum) + ": Decs is being declared a second time without a subroutine."
def ERROREndStatementMissing(lineNum):
    return "Line "+ str(lineNum) + ": Keyword 'end' should appear in this line"
def ERRORBeginStatementMissing(lineNum):
    return "Line " + str(lineNum) + ": Keyword 'begin' should appear before this line"
def ERROROpenBracketMissing(lineNum):
    return "Line " + str(lineNum) + ": Open bracket should be on this line or the next"
def InvalidType(lineNum, failedType):
    return "Line " + str(lineNum) + ": Type presented " + failedType + " is not valid"
def InvalidVariable(lineNum, failedVar):
    return "Line " + str(lineNum) + ": Variable " + failedVar + " does not exist"
def InvalidAssignmentNoOperator(lineNum):
    return "Line " + str(lineNum) + ": '=' symbol must be separated with a space and be the second element"
def InvalidAssignmentEmptyOperand(lineNum):
    return "Line " + str(lineNum) + ": No symbols to the right of '=' symbol "
def InvalidAssignmentEmptyOperand1(lineNum):
    return "Line " + str(lineNum) + ": '=' symbol must be separated with a space and be the second element"
def InvalidArithmeticType(lineNum):
    return "Line " + str(lineNum) + ": Arithmetic requires storage in float or int"
def IfConditionInvalid(lineNum):
    return "Line " + str(lineNum) + ": If condition formated improperly. Please ensure condition is between ( and )"
def WhileConditionInvalid(lineNum):
    return "Line " + str(lineNum) + ": While condition formated improperly. Please ensure condition is between ( and )"

    # def validatedecsOpenBracket(line):
#     if line.find('[') > -1:
#         print("they are on the same line")
#     elif str(executionList[i + 1]).find('[') > -1:
#         print("it is one the next line")