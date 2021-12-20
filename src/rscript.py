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
from typing import List
from rtoken import RToken


class RScript:
    """TODO Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self, script_str: str) -> None:
        pass
    
    @staticmethod
    def get_lst_lexemes(script_str: str) -> List[str]:
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
        lexemes: List[str] = []
        if not script_str:
            return lexemes
        
        lexeme: str = ''
        is_single_bracket: List[bool] = []

        for char_new in script_str:
            """ keep adding characters to the lexeme, one at a time, 
                until we reach a character that would make the lexeme invalid"""
            if RToken.is_valid_lexeme(lexeme + char_new) \
                    and not ((lexeme + char_new) == ']]' \
                             and (len(is_single_bracket) < 1 or is_single_bracket[-1])):
                lexeme += char_new
                continue
            
            """ Edge case: We need to handle nested operator brackets e.g. 'k[[l[[m[6]]]]]'. 
                    For the above example, we need to recognise that the ']' to the right 
                    of '6' is a single ']' bracket and is not part of a double ']]' bracket.
                    To achieve this, we push each open bracket to a stack so that we know 
                    which type of closing bracket is expected for each open bracket."""
            match lexeme:
                case '[':
                    is_single_bracket.append(True)
                case'[[':
                    is_single_bracket.append(False)
                case ']' | ']]':
                    if len(is_single_bracket) < 1:
                        raise Exception("Closing bracket detected ('" + lexeme \
                                + "') with no corresponding open bracket.")
                    is_single_bracket.pop()

            """ adding the new char to the lexeme would make the lexeme invalid, 
                    so we add the existing lexeme to the list and start a new lexeme"""
            lexemes.append(lexeme)
            lexeme = char_new

        lexemes.append(lexeme)
        return lexemes 


