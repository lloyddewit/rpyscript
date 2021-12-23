class clsRToken(object):
    class typToken:
        RSyntacticName = 0
        RFunctionName = 0
        RKeyWord = 0
        RConstantString = 0
        RComment = 0
        RSpace = 0
        RBracket = 0
        RSeparator = 0
        REndStatement = 0
        REndScript = 0
        RNewLine = 0
        ROperatorUnaryLeft = 0
        ROperatorUnaryRight = 0
        ROperatorBinary = 0
        ROperatorBracket = 0
        RPresentation = 0
        RInvalid = 0
    def __init__(self, strLexemePrev, strLexemeCurrent, strLexemeNext, bLexemeNextOnSameLine):
        self.enuToken = None
        self.lstTokens = List[clsRToken]()
        if str.IsNullOrEmpty(strLexemeCurrent):
            return
        strTxt = strLexemeCurrent
        if clsRToken.IsKeyWord(strLexemeCurrent):
            enuToken = clsRToken.typToken.RKeyWord
        elif clsRToken.IsSyntacticName(strLexemeCurrent):
            if ((((strLexemeNext == "(")) and bLexemeNextOnSameLine)):
                enuToken = clsRToken.typToken.RFunctionName
            else:
                enuToken = clsRToken.typToken.RSyntacticName
        elif clsRToken.IsComment(strLexemeCurrent):
            enuToken = clsRToken.typToken.RComment
        elif clsRToken.IsConstantString(strLexemeCurrent):
            enuToken = clsRToken.typToken.RConstantString
        elif clsRToken.IsNewLine(strLexemeCurrent):
            enuToken = clsRToken.typToken.RNewLine
        elif ((strLexemeCurrent == ";")):
            enuToken = clsRToken.typToken.REndStatement
        elif ((strLexemeCurrent == ",")):
            enuToken = clsRToken.typToken.RSeparator
        elif clsRToken.IsSequenceOfSpaces(strLexemeCurrent):
            enuToken = clsRToken.typToken.RSpace
        elif clsRToken.IsBracket(strLexemeCurrent):
            if ((strLexemeCurrent == "}")):
                enuToken = clsRToken.typToken.REndScript
            else:
                enuToken = clsRToken.typToken.RBracket
        elif clsRToken.IsOperatorBrackets(strLexemeCurrent):
            enuToken = clsRToken.typToken.ROperatorBracket
        elif ((clsRToken.IsOperatorUnary(strLexemeCurrent) and ((str.IsNullOrEmpty(strLexemePrev) or (not Regex.IsMatch(strLexemePrev, "[a-zA-Z0-9_\\.)\\]]$")))))):
            enuToken = clsRToken.typToken.ROperatorUnaryRight
        elif ((((strLexemeCurrent == "~")) and ((str.IsNullOrEmpty(strLexemeNext) or (((not bLexemeNextOnSameLine) or (not Regex.IsMatch(strLexemeNext, "^[a-zA-Z0-9_\\.(\\+\\-\\!~]")))))))):
            enuToken = clsRToken.typToken.ROperatorUnaryLeft
        elif ((clsRToken.IsOperatorReserved(strLexemeCurrent) or Regex.IsMatch(strLexemeCurrent, "^%.*%$"))):
            enuToken = clsRToken.typToken.ROperatorBinary
        else:
            enuToken = clsRToken.typToken.RInvalid
    def CloneMe(self):
        clsToken = clsRToken(strTxt, enuToken)
        for clsTokenChild in lstTokens:
            if ((clsTokenChild == None)):
                raise System.Exception("Token has illegal empty child.")
            clsToken.lstTokens.Add(clsTokenChild.CloneMe)
        return clsToken
    @staticmethod
    def IsValidLexeme(strTxt):
        if str.IsNullOrEmpty(strTxt):
            return False
        if (((((not ((strTxt == "\
\
"))) and Regex.IsMatch(strTxt, ".+\\n$"))) or ((Regex.IsMatch(strTxt, ".+\\r$") or ((Regex.IsMatch(strTxt, "^%.*%.+") or ((Regex.IsMatch(strTxt, "^\'.*\'.+") or ((Regex.IsMatch(strTxt, "^\".*\".+") or Regex.IsMatch(strTxt, "^`.*`.+"))))))))))):
            return False
        if ((clsRToken.IsSyntacticName(strTxt) or ((clsRToken.IsOperatorReserved(strTxt) or ((clsRToken.IsOperatorBrackets(strTxt) or ((((strTxt == "<<")) or ((clsRToken.IsNewLine(strTxt) or ((((strTxt == ",")) or ((((strTxt == ";")) or ((clsRToken.IsBracket(strTxt) or ((clsRToken.IsSequenceOfSpaces(strTxt) or ((clsRToken.IsConstantString(strTxt) or ((clsRToken.IsOperatorUserDefined(strTxt) or clsRToken.IsComment(strTxt))))))))))))))))))))))):
            return True
        return False
    @staticmethod
    def IsSyntacticName(strTxt):
        if str.IsNullOrEmpty(strTxt):
            return False
        return ((Regex.IsMatch(strTxt, "^[a-zA-Z0-9_\\.]+$") or Regex.IsMatch(strTxt, "^`.*")))
    @staticmethod
    def IsConstantString(strTxt):
        if (((not str.IsNullOrEmpty(strTxt)) and ((Regex.IsMatch(strTxt, "^\".*") or Regex.IsMatch(strTxt, "^\'.*"))))):
            return True
        return False
    @staticmethod
    def IsComment(strTxt):
        if (((not str.IsNullOrEmpty(strTxt)) and Regex.IsMatch(strTxt, "^#.*"))):
            return True
        return False
    @staticmethod
    def IsSequenceOfSpaces(strTxt):
        if (((not str.IsNullOrEmpty(strTxt)) and (((not ((strTxt == "\
"))) and Regex.IsMatch(strTxt, "^ *$"))))):
            return True
        return False
    @staticmethod
    def IsElement(strTxt):
        if (not ((str.IsNullOrEmpty(strTxt) or ((clsRToken.IsNewLine(strTxt) or ((clsRToken.IsSequenceOfSpaces(strTxt) or clsRToken.IsComment(strTxt)))))))):
            return True
        return False
    @staticmethod
    def IsOperatorUserDefined(strTxt):
        if (((not str.IsNullOrEmpty(strTxt)) and Regex.IsMatch(strTxt, "^%.*"))):
            return True
        return False
    @staticmethod
    def IsOperatorReserved(strTxt):
        "::"
        ":::"
        "$"
        "@"
        "^"
        ":"
        "%%"
        "%/%"
        "%*%"
        "%o%"
        "%x%"
        "%in%"
        "/"
        "*"
        "+"
        "-"
        "<"
        ">"
        "<="
        ">="
        "=="
        "!="
        "!"
        "&"
        "&&"
        "|"
        "||"
        "~"
        "->"
        "->>"
        "<-"
        "<<-"
        "="
        return arrROperators.Contains(strTxt)
    @staticmethod
    def IsOperatorBrackets(strTxt):
        "["
        "]"
        "[["
        "]]"
        return arrROperatorBrackets.Contains(strTxt)
    @staticmethod
    def IsOperatorUnary(strTxt):
        "+"
        "-"
        "!"
        "~"
        return arrROperatorUnary.Contains(strTxt)
    @staticmethod
    def IsBracket(strTxt):
        "("
        ")"
        "{"
        "}"
        return arrRBrackets.Contains(strTxt)
    @staticmethod
    def IsNewLine(strTxt):
        "\
"
        "\
"
        "\
\
"
        return arrRNewLines.Contains(strTxt)
    @staticmethod
    def IsKeyWord(strTxt):
        "if"
        "else"
        "repeat"
        "while"
        "function"
        "for"
        "in"
        "next"
        "break"
        return arrKeyWords.Contains(strTxt)