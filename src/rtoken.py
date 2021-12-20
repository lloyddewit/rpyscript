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
import re

class RToken:
    """TODO Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def is_valid_lexeme(txt: str) -> bool:
        """
        Returns true if txt is a valid lexeme, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a valid lexeme, else false.
        """
        if not txt:
            return False

        """ string is not a valid lexeme if string is:
                >1 char and ends in newline (but \r\n is a valid lexeme)
                >1 char and ends in carriage return
                a user-defined operator followed by another character
                a single quoted string followed by another character
                a double quoted string followed by another character
                a backtick quoted string followed by another character """
        if (re.search('.+\n$', txt) and txt != '\r\n') \
                or re.search('.+\r$', txt) \
                or re.search('^%%.*%%.+', txt) \
                or re.search("^'.*'.+", txt) \
                or re.search('^".*".+', txt) \
                or re.search('^`.*`.+', txt):
            return False
        
        """ string is a valid lexeme if string is:
                a syntactic name or reserved word
                an operator (e.g. '+')
                a bracket operator (e.g. '[')
                a partial operator (e.g. ':')
                a newline (e.g. '\n')
                a parameter separator or end statement
                a bracket (e.g. '{')
                a sequence of spaces
                a string constant (starts with a single or double quote)
                a user-defined operator (starts with '%*')
                a comment (starts with '#*')"""
        if RToken.is_syntactic_name(txt) \
                or RToken.is_operator_reserved(txt) \
                or RToken.is_operator_brackets(txt) \
                or txt == '<<' \
                or RToken.is_newline(txt) \
                or txt == ',' or txt == ';' \
                or RToken.is_bracket(txt) \
                or RToken.is_sequence_of_spaces(txt) \
                or RToken.is_constant_string(txt) \
                or RToken.is_operator_user_defined(txt) \
                or RToken.is_comment(txt):
            return True

        """ if the string is not covered by any of the checks above, 
                then we assume by default, that it's not a valid lexeme"""
        return False

    @staticmethod
    def is_syntactic_name(txt: str) -> bool:
        """
        Returns true if txt is a complete or partial valid R syntactic name or keyword, 
        else returns false.
        Please note that the rules for syntactic names are actually stricter than the rules used 
        in this function, but this library assumes it is parsing valid R code.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a valid R syntactic name or keyword, else false.
        """
        return re.search('^[a-zA-Z0-9_.]+$', txt) != None \
            or re.search('^`.*', txt) != None
        
    @staticmethod
    def is_constant_string(txt: str) -> bool:
        """
        Returns true if txt is a complete or partial string constant, else returns false.
        String constants are delimited by a pair of single (') or double (") quotes and can contain
        all other printable characters. Quotes and other special characters within strings are 
        specified using escape sequences.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a a complete or partial string constant, else false.
        """
        return re.search('^".*', txt) != None \
            or re.search("^'.*", txt) != None
        
    @staticmethod
    def is_comment(txt: str) -> bool:
        """
        Returns true if txt is a comment, else returns false.
        Any text from a # character to the end of the line is taken to be a comment. 
        The only exception is if the # character is inside a quoted string. This function does not
        test for this exception. The user must test for this separately.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a comment, else false.
        """
        return re.search('^#.*', txt) != None
        
    @staticmethod
    def is_sequence_of_spaces(txt: str) -> bool:
        """
        Returns true if txt is sequence of spaces (and no other characters), else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is sequence of spaces (and no other characters), else false.
        """
        return txt != '\n' and re.search('^ *$', txt) != None
        
    @staticmethod
    def is_element(txt: str) -> bool:
        """
        Returns true if txt is a complete or partial functional R element (i.e. not empty, 
        and not a space, comment or new line), else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a complete or partial functional R element (i.e. not empty, 
            and not a space, comment or new line), else false.
        """
        return not (RToken.is_newline(txt) \
                or RToken.is_sequence_of_spaces(txt) \
                or RToken.is_comment(txt))

    @staticmethod
    def is_operator_user_defined(txt: str) -> bool:
        """
        Returns true if txt is a complete or partial user-defined operator, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a complete or partial user-defined operator, else false.
        """
        return re.search('^%.*', txt) != None        

    @staticmethod
    def is_operator_reserved(txt: str) -> bool:
        """
        Returns true if txt is a resrved operator, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a resrved operator, else false.
        """
        return txt in ('::', ':::', '$', '@', '^', ':', '%%%%', '%%/%%', '%%*%%', '%%o%%', '%%x%%', 
                        '%%in%%', '/', '*', '+', '-', '<', '>', '<=', '>=', '==', '!=', '!', '&', 
                        '&&', '|', '||', '~', '->', '->>', '<-', '<<-', '=')
        
    @staticmethod
    def is_operator_brackets(txt: str) -> bool:
        """
        Returns true if txt is a bracket operator, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a bracket operator, else false.
        """
        return txt in ('[', ']', '[[', ']]')

    @staticmethod
    def is_operator_unary(txt: str) -> bool:
        """
        Returns true if txt is a unary operator, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a unary operator, else false.
        """
        return txt in ('+', '-', '!', '~')

    @staticmethod
    def is_bracket(txt: str) -> bool:
        """
        Returns true if txt is a bracket, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a bracket, else false.
        """
        return txt in ('(', ')', '{', '}')

    @staticmethod
    def is_newline(txt: str) -> bool:
        """
        Returns true if txt is a newline, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a newline, else false.
        """
        return txt in ('\r', '\n', '\r\n')

    @staticmethod
    def is_keyword(txt: str) -> bool:
        """
        Returns true if txt is a keyword, else returns false.

        Args:
            txt: A sequence of characters from a syntactically correct R script.

        Returns
            True if txt is a keyword, else false.
        """
        return txt in ('if', 'else', 'repeat', 'while', 'function', 'for', 'in', 'next', 'break')
