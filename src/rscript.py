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
import rlexeme
import rtoken
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
        self.tokens: List[rtoken.RToken] = []
        self.statements: List[RStatement] = []        
        self.assignments: Dict[str, RStatement] = {}

        if not script_str:
            return

        self.tokens: List[rtoken.RToken] = rtoken.get_tokens(rlexeme.get_lexemes(script_str))
        pos: int = 0
        while pos < len(self.tokens):
            statement: RStatement = RStatement()
            pos = statement.set_from_tokens(self.tokens, pos, self.assignments)
            self.statements.append(statement)
            if statement.assignment:
                self.assignments[statement.assignment.text] = statement
     
    def get_as_executable_script(self) -> str:
        text = ''
        for statement in self.statements:
            text += statement.get_as_executable_script()
        return text
