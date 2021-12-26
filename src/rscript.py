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

    def __init__(self, script_str: str) -> None:
        self.statements = List[clsRStatement]()
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
    
    def GetAsExecutableScript(self):
        strTxt = ""
        for clsStatement in lstRStatements:
            clsStatement.GetAsExecutableScript()
        return strTxt


    


