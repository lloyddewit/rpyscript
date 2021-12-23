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
from _typeshed import Self
from typing import List
from collections import deque
from enum import Enum
import re

import rlexeme

class TokenState(Enum):
    WAITING_FOR_OPEN_CONDITION = 1
    WAITING_FOR_CLOSE_CONDITION = 2 
    WAITING_FOR_START_SCRIPT = 3 
    WAITING_FOR_END_SCRIPT = 4

class TokenType(Enum):
    SYNTACTIC_NAME = 1
    FUNCTION_NAME =2
    KEY_WORD = 3
    CONSTANT_STRING = 4
    COMMENT = 5
    SPACE = 6
    BRACKET = 7
    SEPARATOR = 8
    END_STATEMENT = 9
    END_SCRIPT = 10
    NEW_LINE = 11
    OPERATOR_UNARY_LEFT = 12
    OPERATOR_UNARY_RIGHT = 13
    OPERATOR_BINARY = 14
    OPERATOR_BRACKET = 15
    PRESENTATION = 16
    INVALID = 17

class RToken:
    """TODO Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, lexeme_prev, lexeme_current, lexeme_next, lexeme_next_on_same_line) -> None:
        self.enuToken = None
        #self.lstTokens = List[clsRToken]()
        if not lexeme_current:
            return

        strTxt = lexeme_current
        if rlexeme.is_keyword(lexeme_current):
            enuToken = TokenType.KEY_WORD
        elif rlexeme.is_syntactic_name(lexeme_current):
            if lexeme_next == "(" and lexeme_next_on_same_line:
                enuToken = TokenType.FUNCTION_NAME
            else:
                enuToken = TokenType.SYNTACTIC_NAME
        elif rlexeme.is_comment(lexeme_current):
            enuToken = TokenType.COMMENT
        elif rlexeme.is_constant_string(lexeme_current):
            enuToken = TokenType.CONSTANT_STRING
        elif rlexeme.is_newline(lexeme_current):
            enuToken = TokenType.NEW_LINE
        elif lexeme_current == ";":
            enuToken = TokenType.END_STATEMENT
        elif lexeme_current == ",":
            enuToken = TokenType.SEPARATOR
        elif rlexeme.is_sequence_of_spaces(lexeme_current):
            enuToken = TokenType.SPACE
        elif rlexeme.is_bracket(lexeme_current):
            if lexeme_current == "}":
                enuToken = TokenType.END_SCRIPT
            else:
                enuToken = TokenType.BRACKET
        elif rlexeme.is_operator_brackets(lexeme_current):
            enuToken = TokenType.OPERATOR_BRACKET
        elif rlexeme.is_operator_unary(lexeme_current) and not lexeme_prev or not re.search('[a-zA-Z0-9_\\.)\\]]$', lexeme_prev):
            enuToken = TokenType.OPERATOR_UNARY_RIGHT
        elif lexeme_current == "~" and not lexeme_next or not lexeme_next_on_same_line or not re.search('^[a-zA-Z0-9_\\.(\\+\\-\\!~]', lexeme_next):
            enuToken = TokenType.OPERATOR_UNARY_LEFT
        elif rlexeme.is_operator_reserved(lexeme_current) or re.search("^%.*%$", lexeme_current):
            enuToken = TokenType.OPERATOR_BINARY
        else:
            enuToken = TokenType.INVALID

def get_tokens(lexemes: List[str]) -> List[RToken]:
    tokens : List[RToken] = []
    if not lexemes or len(lexemes) < 1:
        return tokens

    lexeme_prev: str = ""
    lexeme_current: str = ""
    statement_contains_element: bool = False

    num_open_brackets_stack: List[int] = [] 
    num_open_brackets_stack.append(0)
    is_script_enclosed_by_curly_brackets_stack: List[bool] = []
    is_script_enclosed_by_curly_brackets_stack.append(True)
    token_state_stack: List[TokenState] = []
    token_state_stack.append(TokenState.WAITING_FOR_START_SCRIPT)

    pos = 0
    while pos <= len(lexemes) - 1:

        if len(num_open_brackets_stack) < 1:
            raise Exception("The stack storing the number of open brackets must have at least one value.")
        elif len(is_script_enclosed_by_curly_brackets_stack) < 1:
            raise Exception("The stack storing the number of open curly brackets must have at least one value.")
        elif len(token_state_stack) < 1:
            raise Exception("The stack storing the current state of the token parsing must have at least one value.")

        # store previous non-space lexeme
        if rlexeme.is_element(lexeme_current):
            lexeme_prev = lexeme_current

        lexeme_current = lexemes[pos]
        if not statement_contains_element:
            statement_contains_element = rlexeme.is_element(lexeme_current)
        
        # find next lexeme that represents an R element
        lexeme_next: str  = ""
        lexeme_next_on_same_line: bool = True
        next_pos: int = pos + 1
        while next_pos <= len(lexemes) - 1:
            if rlexeme.is_element(lexemes[next_pos]):
                lexeme_next = lexemes[next_pos]
                break
            if lexemes[next_pos] == "\n" or lexemes[next_pos] == "\r":
                lexeme_next_on_same_line = False
            next_pos += 1

        """ determine whether the current sequence of tokens makes a complete valid R statement
                This is needed to determine whether a newline marks the end of the statement
                or is just for presentation.
                The current sequence of tokens is considered a complete valid R statement if it 
                has no open brackets and it does not end in an operator.
        """
        match lexeme_current:
            case '(' | '[' | '[[':
                num_open_brackets_stack.append(num_open_brackets_stack.pop() + 1)
            case ')' | ']' | ']]':
                num_open_brackets_stack.append(num_open_brackets_stack.pop() - 1)
            case 'if' | 'while' | 'for' | 'function':
                token_state_stack.append(TokenState.WAITING_FOR_OPEN_CONDITION)
                num_open_brackets_stack.append(0)
            case 'else' | 'repeat':
                """ else' and 'repeat' keywords have no condition (e.g. 'if (x==1) y<-0 else y<-1'
                        after the keyword is processed, the state will automatically change to WAITING_FOR_END_SCRIPT
                """
                token_state_stack.append(TokenState.WAITING_FOR_CLOSE_CONDITION)
                num_open_brackets_stack.append(0)

        # identify the token associated with the current lexeme and add the token to the list
        clsToken = clsRToken(lexeme_prev, lexeme_current, lexeme_next, lexeme_next_on_same_line)

        """ Process key words
                Determine whether the next end statement will also be the end of the current script.
                Normally, a '}' indicates the end of the current script. However, R allows single
                statement scripts, not enclosed with '{}' for selected key words. 
                The key words that allow this are: if, else, while, for and function.
                For example:
                    if(x <= 0) y <- log(1+x) else y <- log(x)
        """
        if clsToken.enuToken == TokenType.COMMENT or clsToken.enuToken == TokenType.SPACE:
            pass
        else:
            if token_state_stack[-1] == TokenState.WAITING_FOR_OPEN_CONDITION:
                if (not clsToken.enuToken == TokenType.NEW_LINE):
                    if clsToken.strTxt == "(":
                        token_state_stack.pop()
                        token_state_stack.append(TokenState.WAITING_FOR_CLOSE_CONDITION)
            elif token_state_stack[-1] == TokenState.WAITING_FOR_CLOSE_CONDITION:
                if num_open_brackets_stack[-1] == 0:
                    token_state_stack.pop()
                    token_state_stack.append(TokenState.WAITING_FOR_START_SCRIPT)
            elif token_state_stack[-1] == TokenState.WAITING_FOR_START_SCRIPT:
                if (not clsToken.enuToken == TokenType.COMMENT or clsToken.enuToken == TokenType.PRESENTATION or clsToken.enuToken == TokenType.SPACE or clsToken.enuToken == TokenType.NEW_LINE):
                    token_state_stack.pop()
                    token_state_stack.append(TokenState.WAITING_FOR_END_SCRIPT)
                    if clsToken.strTxt == "{":
                        is_script_enclosed_by_curly_brackets_stack.append(True)
                    else:
                        is_script_enclosed_by_curly_brackets_stack.append(False)
            elif token_state_stack[-1] == TokenState.WAITING_FOR_END_SCRIPT:
                if clsToken.enuToken == TokenType.NEW_LINE and statement_contains_element and num_open_brackets_stack[-1] == 0 and not rlexeme.is_operator_user_defined(lexeme_prev and (not rlexeme.is_operator_reserved(lexeme_prev) and (not lexeme_prev == "~":
                    clsToken.enuToken = TokenType.END_STATEMENT
                    statement_contains_element = False
                if clsToken.enuToken == TokenType.END_STATEMENT and is_script_enclosed_by_curly_brackets_stack[-1] == False and str.IsNullOrEmpty(strLexemeNext):
                    clsToken.enuToken = TokenType.END_SCRIPT
                if clsToken.enuToken == TokenType.END_SCRIPT:
                    is_script_enclosed_by_curly_brackets_stack.pop()
                    num_open_brackets_stack.pop()
                    token_state_stack.pop()
            else:
                raise Exception("The token is in an unknown state.")
        lstRTokens.Add(clsToken)
        if clsToken.enuToken == TokenType.END_SCRIPT and str.IsNullOrEmpty(strLexemeNext):
            return lstRTokens
        pos += 1

    return tokens

def get_tokens_as_string(tokens: List[RToken]) -> str:
    tokens_str : str = ""
    return tokens_str
