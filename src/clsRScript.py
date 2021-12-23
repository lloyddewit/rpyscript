class clsRScript(object):
    class typTokenState:
        WaitingForOpenCondition = 0
        WaitingForCloseCondition = 0
        WaitingForStartScript = 0
        WaitingForEndScript = 0
    def __init__(self, strInput):
        self.lstRStatements = List[clsRStatement]()
        if str.IsNullOrEmpty(strInput):
            return
        lstLexemes = self.GetLstLexemes(strInput)
        lstTokens = self.GetLstTokens(lstLexemes)
        intPos = 0
        dctAssignments = Dictionary[(str, clsRStatement)]()
        while ((intPos < lstTokens.Count)):
            clsStatement = clsRStatement(lstTokens, intPos, dctAssignments)
            lstRStatements.Add(clsStatement)
            if (not ((clsStatement.clsAssignment == None))):
                if dctAssignments.ContainsKey(clsStatement.clsAssignment.strTxt):
                    dctAssignments(clsStatement.clsAssignment.strTxt) = clsStatement
                else:
                    dctAssignments.Add(clsStatement.clsAssignment.strTxt, clsStatement)
    def GetLstLexemes(self, strRScript):
        if str.IsNullOrEmpty(strRScript):
            return None
        lstLexemes = List[str]()
        strTxt = None
        stkIsSingleBracket = Stack[bool]()
        for chrNew in strRScript:
            if ((clsRToken.IsValidLexeme(((strTxt + chrNew))) and (not ((((((strTxt + chrNew)) == "]]")) and ((((stkIsSingleBracket.Count < 1)) or stkIsSingleBracket.Peek()))))))):
                chrNew
            if ((strTxt == "[")):
                stkIsSingleBracket.Push(True)
            elif ((strTxt == "[[")):
                stkIsSingleBracket.Push(False)
            elif (((strTxt == "]")) or ((strTxt == "]]"))):
                if ((stkIsSingleBracket.Count < 1)):
                    raise System.Exception((("Closing bracket detected (\'" + ((strTxt + "\') with no corresponding open bracket.")))))
                stkIsSingleBracket.Pop()
            lstLexemes.Add(strTxt)
            strTxt = chrNew
        lstLexemes.Add(strTxt)
        return lstLexemes
    def GetLstTokens(self, lstLexemes):
        if ((((lstLexemes == None)) or ((lstLexemes.Count == 0)))):
            return None
        lstRTokens = List[clsRToken]()
        strLexemePrev = ""
        strLexemeCurrent = ""
        bStatementContainsElement = False
        stkNumOpenBrackets = Stack[int]()
        stkNumOpenBrackets.Push(0)
        stkIsScriptEnclosedByCurlyBrackets = Stack[bool]()
        stkIsScriptEnclosedByCurlyBrackets.Push(True)
        stkTokenState = Stack[typTokenState]()
        stkTokenState.Push(typTokenState.WaitingForStartScript)
        intPos = 0
        while ((intPos <= ((lstLexemes.Count - 1)))):
            if ((stkNumOpenBrackets.Count < 1)):
                raise System.Exception("The stack storing the number of open brackets must have at least one value.")
            elif ((stkIsScriptEnclosedByCurlyBrackets.Count < 1)):
                raise System.Exception("The stack storing the number of open curly brackets must have at least one value.")
            elif ((stkTokenState.Count < 1)):
                raise System.Exception("The stack storing the current state of the token parsing must have at least one value.")
            if clsRToken.IsElement(strLexemeCurrent):
                strLexemePrev = strLexemeCurrent
            strLexemeCurrent = lstLexemes.Item[intPos]
            bStatementContainsElement
            bStatementContainsElement
            clsRToken.IsElement(strLexemeCurrent)
            strLexemeNext = None
            bLexemeNextOnSameLine = True
            intNextPos = ((intPos + 1))
            while ((intNextPos <= ((lstLexemes.Count - 1)))):
                if clsRToken.IsElement(lstLexemes.Item[intNextPos]):
                    strLexemeNext = lstLexemes.Item[intNextPos]
                    break
                if ((((lstLexemes.Item[intNextPos] == "\
")) or ((lstLexemes.Item[intNextPos] == "\
"))) or ((lstLexemes.Item[intNextPos] == "\
"))):
                    bLexemeNextOnSameLine = False
                intNextPos += 1
            if ((((strLexemeCurrent == "(")) or ((strLexemeCurrent == "["))) or ((strLexemeCurrent == "[["))):
                stkNumOpenBrackets.Push(((stkNumOpenBrackets.Pop() + 1)))
            elif ((((strLexemeCurrent == ")")) or ((strLexemeCurrent == "]"))) or ((strLexemeCurrent == "]]"))):
                stkNumOpenBrackets.Push(((stkNumOpenBrackets.Pop() - 1)))
            elif (((((strLexemeCurrent == "if")) or ((strLexemeCurrent == "while"))) or ((strLexemeCurrent == "for"))) or ((strLexemeCurrent == "function"))):
                stkTokenState.Push(typTokenState.WaitingForOpenCondition)
                stkNumOpenBrackets.Push(0)
            elif (((strLexemeCurrent == "else")) or ((strLexemeCurrent == "repeat"))):
                stkTokenState.Push(typTokenState.WaitingForCloseCondition)
                stkNumOpenBrackets.Push(0)
            clsToken = clsRToken(strLexemePrev, strLexemeCurrent, strLexemeNext, bLexemeNextOnSameLine)
            if ((((clsToken.enuToken == clsRToken.typToken.RComment)) or ((clsToken.enuToken == clsRToken.typToken.RSpace)))):
                pass
            else:
                if ((stkTokenState.Peek() == typTokenState.WaitingForOpenCondition)):
                    if (not ((clsToken.enuToken == clsRToken.typToken.RNewLine))):
                        if ((clsToken.strTxt == "(")):
                            stkTokenState.Pop()
                            stkTokenState.Push(typTokenState.WaitingForCloseCondition)
                elif ((stkTokenState.Peek() == typTokenState.WaitingForCloseCondition)):
                    if ((stkNumOpenBrackets.Peek() == 0)):
                        stkTokenState.Pop()
                        stkTokenState.Push(typTokenState.WaitingForStartScript)
                elif ((stkTokenState.Peek() == typTokenState.WaitingForStartScript)):
                    if (not ((((clsToken.enuToken == clsRToken.typToken.RComment)) or ((((clsToken.enuToken == clsRToken.typToken.RPresentation)) or ((((clsToken.enuToken == clsRToken.typToken.RSpace)) or ((clsToken.enuToken == clsRToken.typToken.RNewLine))))))))):
                        stkTokenState.Pop()
                        stkTokenState.Push(typTokenState.WaitingForEndScript)
                        if ((clsToken.strTxt == "{")):
                            stkIsScriptEnclosedByCurlyBrackets.Push(True)
                        else:
                            stkIsScriptEnclosedByCurlyBrackets.Push(False)
                elif ((stkTokenState.Peek() == typTokenState.WaitingForEndScript)):
                    if ((((clsToken.enuToken == clsRToken.typToken.RNewLine)) and ((bStatementContainsElement and ((((stkNumOpenBrackets.Peek() == 0)) and (((not clsRToken.IsOperatorUserDefined(strLexemePrev)) and (not ((clsRToken.IsOperatorReserved(strLexemePrev) and (not ((strLexemePrev == "~")))))))))))))):
                        clsToken.enuToken = clsRToken.typToken.REndStatement
                        bStatementContainsElement = False
                    if ((((clsToken.enuToken == clsRToken.typToken.REndStatement)) and ((((stkIsScriptEnclosedByCurlyBrackets.Peek() == False)) and str.IsNullOrEmpty(strLexemeNext))))):
                        clsToken.enuToken = clsRToken.typToken.REndScript
                    if ((clsToken.enuToken == clsRToken.typToken.REndScript)):
                        stkIsScriptEnclosedByCurlyBrackets.Pop()
                        stkNumOpenBrackets.Pop()
                        stkTokenState.Pop()
                else:
                    raise System.Exception("The token is in an unknown state.")
            lstRTokens.Add(clsToken)
            if ((((clsToken.enuToken == clsRToken.typToken.REndScript)) and str.IsNullOrEmpty(strLexemeNext))):
                return lstRTokens
            intPos += 1
        return lstRTokens
    def GetAsExecutableScript(self):
        strTxt = ""
        for clsStatement in lstRStatements:
            clsStatement.GetAsExecutableScript()
        return strTxt
