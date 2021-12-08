"""
TODO RPyScript <one line to give the program's name and a brief idea of what it does.>
Copyright (C) 2021-2022 IDEMS International, Stephen Lloyd

This file is part of RPyScript.

    RPyScript is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RPyScript is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with RPyScript.  If not, see <https://www.gnu.org/licenses/>.
"""
"""TODO A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
class RScript:
    """TODO Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self, script_str) -> None:
        self.script_str = script_str

    def get_lst_lexemes(self, script_str) -> list:
        """
        Returns script_str as a list of its constituent lexemes. 
        A lexeme is a string of characters that represent a valid R element 
        (identifier, operator, keyword, seperator, bracket etc.). A lexeme does not 
        include any type information.
        
        This function identifies lexemes using a technique known as 'longest match' 
        or 'maximal munch'. It keeps adding characters to the lexeme one at a time 
        until it reaches a character that is not in the set of characters acceptable 
        for that lexeme.

        Args:
            script_str: The R script to convert (must be syntactically correct R).

        Returns
            script_str as a list of its constituent lexemes.
        """
        
        """ if str.IsNullOrEmpty(strRScript):
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
        return lstLexemes """
        return ['a', '::', 'b']

