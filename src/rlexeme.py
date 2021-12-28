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
import re

def get_lexemes(script_str: str) -> List[str]:
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
        if is_valid_lexeme(lexeme + char_new) \
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
    if is_syntactic_name(txt) \
            or is_operator_reserved(txt) \
            or is_operator_brackets(txt) \
            or txt == '<<' \
            or is_newline(txt) \
            or txt == ',' or txt == ';' \
            or is_bracket(txt) \
            or is_sequence_of_spaces(txt) \
            or is_constant_string(txt) \
            or is_operator_user_defined(txt) \
            or is_comment(txt):
        return True

    """ if the string is not covered by any of the checks above, 
            then we assume by default, that it's not a valid lexeme"""
    return False


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
    

def is_sequence_of_spaces(txt: str) -> bool:
    """
    Returns true if txt is sequence of spaces (and no other characters), else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is sequence of spaces (and no other characters), else false.
    """
    return txt != '\n' and re.search('^ *$', txt) != None
    

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
    return not (is_newline(txt) \
            or is_sequence_of_spaces(txt) \
            or is_comment(txt))


def is_operator_user_defined(txt: str) -> bool:
    """
    Returns true if txt is a complete or partial user-defined operator, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a complete or partial user-defined operator, else false.
    """
    return re.search('^%.*', txt) != None        


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
    

def is_operator_brackets(txt: str) -> bool:
    """
    Returns true if txt is a bracket operator, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a bracket operator, else false.
    """
    return txt in ('[', ']', '[[', ']]')


def is_operator_unary(txt: str) -> bool:
    """
    Returns true if txt is a unary operator, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a unary operator, else false.
    """
    return txt in ('+', '-', '!', '~')


def is_bracket(txt: str) -> bool:
    """
    Returns true if txt is a bracket, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a bracket, else false.
    """
    return txt in ('(', ')', '{', '}')


def is_newline(txt: str) -> bool:
    """
    Returns true if txt is a newline, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a newline, else false.
    """
    return txt in ('\r', '\n', '\r\n')


def is_keyword(txt: str) -> bool:
    """
    Returns true if txt is a keyword, else returns false.

    Args:
        txt: A sequence of characters from a syntactically correct R script.

    Returns
        True if txt is a keyword, else false.
    """
    return txt in ('if', 'else', 'repeat', 'while', 'function', 'for', 'in', 'next', 'break')
