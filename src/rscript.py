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

from typing import Dict, List
from rtoken import RToken
from rstatement import RStatement


class RScript(object):
    """TODO Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, script_str: str) -> None:
        if not script_str:
            return

        self.tokens: List[RToken] = []
        self.statements: List[RStatement] = []        
        pos = 0
        assignments: Dict[str, RStatement] = {}
"""         while pos < len(self.tokens):
            clsStatement: clsRStatement = RStatement(self.tokens, pos, assignments)
            self.statements.append(clsStatement)
            if (not ((clsStatement.clsAssignment == None))):
                if assignments.ContainsKey(clsStatement.clsAssignment.strTxt):
                    assignments(clsStatement.clsAssignment.strTxt) = clsStatement
                else:
                    assignments.Add(clsStatement.clsAssignment.strTxt, clsStatement)
     
    def GetAsExecutableScript(self):
        strTxt = ""
        for clsStatement in self.statements:
            clsStatement.GetAsExecutableScript()
        return strTxt
"""


    


