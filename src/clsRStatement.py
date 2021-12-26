from System.Text.RegularExpressions import *
class clsRStatement(object):
    def __init__(self, lstTokens, intPos, dctAssignments):
        self.bTerminateWithNewline = True
        self.strAssignmentOperator = None
        self.strAssignmentPrefix = None
        self.strSuffix = None
        self.clsAssignment = None
        self.clsElement = None
        self.intOperatorsBrackets = 2
        self.intOperatorsUnaryOnly = 4
        self.intOperatorsUserDefined = 6
        self.intOperatorsTilda = 13
        self.intOperatorsRightAssignment = 14
        self.intOperatorsLeftAssignment1 = 15
        self.intOperatorsLeftAssignment2 = 16
        if ((lstTokens.Count <= 0)):
            return
        arrOperatorPrecedence(0) = ["::", ":::"]
        arrOperatorPrecedence(1) = ["$", "@"]
        arrOperatorPrecedence(intOperatorsBrackets) = ["[", "[["]
        arrOperatorPrecedence(3) = ["^"]
        arrOperatorPrecedence(intOperatorsUnaryOnly) = ["-", "+"]
        arrOperatorPrecedence(5) = [":"]
        arrOperatorPrecedence(intOperatorsUserDefined) = ["%"]
        arrOperatorPrecedence(7) = ["*", "/"]
        arrOperatorPrecedence(8) = ["+", "-"]
        arrOperatorPrecedence(9) = ["<>", "<=", ">=", "==", "!="]
        arrOperatorPrecedence(10) = ["!"]
        arrOperatorPrecedence(11) = ["&", "&&"]
        arrOperatorPrecedence(12) = ["|", "||"]
        arrOperatorPrecedence(intOperatorsTilda) = ["~"]
        arrOperatorPrecedence(intOperatorsRightAssignment) = ["->", "->>"]
        arrOperatorPrecedence(intOperatorsLeftAssignment1) = ["<-", "<<-"]
        arrOperatorPrecedence(intOperatorsLeftAssignment2) = ["="]
        lstStatementTokens = List[clsRToken]()
        while ((intPos < lstTokens.Count)):
            lstStatementTokens.Add(lstTokens.Item[intPos])
            if ((((lstTokens.Item[intPos].enuToken == clsRToken.typToken.REndStatement)) or ((lstTokens.Item[intPos].enuToken == clsRToken.typToken.REndScript)))):
                intPos += 1
                break
            intPos += 1
        lstTokenPresentation = GetLstPresentation(lstStatementTokens, 0)
        lstTokenBrackets = GetLstTokenBrackets(lstTokenPresentation, 0)
        lstTokenFunctionBrackets = GetLstTokenFunctionBrackets(lstTokenBrackets)
        lstTokenCommas = GetLstTokenCommas(lstTokenFunctionBrackets, 0)
        lstTokenTree = GetLstTokenOperators(lstTokenCommas)
        if ((lstTokenTree.Count < 1)):
            raise System.Exception("The token tree must contain at least one token.")
        if ((((lstTokenTree.Item[0].enuToken == clsRToken.typToken.ROperatorBinary)) and ((lstTokenTree.Item[0].lstTokens.Count > 1)))):
            clsTokenChildLeft = lstTokenTree.Item[0].lstTokens.Item(((lstTokenTree.Item[0].lstTokens.Count - 2)))
            clsTokenChildRight = lstTokenTree.Item[0].lstTokens.Item(((lstTokenTree.Item[0].lstTokens.Count - 1)))
            if ((arrOperatorPrecedence(intOperatorsLeftAssignment1).Contains(lstTokenTree.Item[0].strTxt) or arrOperatorPrecedence(intOperatorsLeftAssignment2).Contains(lstTokenTree.Item[0].strTxt))):
                clsAssignment = GetRElement(clsTokenChildLeft, dctAssignments)
                clsElement = GetRElement(clsTokenChildRight, dctAssignments)
            elif arrOperatorPrecedence(intOperatorsRightAssignment).Contains(lstTokenTree.Item[0].strTxt):
                clsAssignment = GetRElement(clsTokenChildRight, dctAssignments)
                clsElement = GetRElement(clsTokenChildLeft, dctAssignments)
        if (not ((clsAssignment == None))):
            strAssignmentOperator = lstTokenTree.Item[0].strTxt
            ((lstTokenTree.Item[0].lstTokens.Item(0).enuToken == clsRToken.typToken.RPresentation))
            lstTokenTree.Item[0].lstTokens.Item(0).strTxt
            ""
        else:
            clsElement = GetRElement(lstTokenTree.Item[0], dctAssignments)
        clsTokenEndStatement = lstTokenTree.Item[((lstTokenTree.Count - 1))]
        if ((((clsTokenEndStatement.enuToken == clsRToken.typToken.REndStatement)) and ((clsTokenEndStatement.strTxt == ";")))):
            bTerminateWithNewline = False
        (((not ((clsElement == None))) and ((((clsTokenEndStatement.lstTokens.Count > 0)) and ((clsTokenEndStatement.lstTokens.Item[0].enuToken == clsRToken.typToken.RPresentation))))))
        clsTokenEndStatement.lstTokens.Item[0].strTxt
        ""
    def GetAsExecutableScript(self):
        strElement = self.GetScriptElement(clsElement)
        if ((((clsAssignment == None)) or str.IsNullOrEmpty(strAssignmentOperator))):
            strScript = strElement
        else:
            strAssigment = self.GetScriptElement(clsAssignment)
            if ((arrOperatorPrecedence(intOperatorsLeftAssignment1).Contains(strAssignmentOperator) or arrOperatorPrecedence(intOperatorsLeftAssignment2).Contains(strAssignmentOperator))):
                strScript = ((strAssigment + ((strAssignmentPrefix + ((strAssignmentOperator + strElement))))))
            elif arrOperatorPrecedence(intOperatorsRightAssignment).Contains(strAssignmentOperator):
                strScript = ((strElement + ((strAssignmentPrefix + ((strAssignmentOperator + strAssigment))))))
            else:
                raise System.Exception("The statement\'s assignment operator is an unknown type.")
        strSuffix
        if bTerminateWithNewline:
            "\
"
            ";"
            return strScript

