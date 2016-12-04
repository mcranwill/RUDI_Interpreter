

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

# def validatedecsOpenBracket(line):
#     if line.find('[') > -1:
#         print("they are on the same line")
#     elif str(executionList[i + 1]).find('[') > -1:
#         print("it is one the next line")