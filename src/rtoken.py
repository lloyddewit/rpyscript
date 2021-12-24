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

    def __init__(self, lexeme_prev: str, lexeme_current: str, lexeme_next: str, lexeme_next_on_same_line: bool) -> None:
        """
        Constructs a token 'lexeme_current'.
        A token is a string of characters that represent a valid R element, plus meta data about
        the token type (identifier, operator, keyword, bracket etc.).
        'lexeme_prev' and 'lexeme_next' are needed to correctly identify if 'lexeme_current' is 
        a unary or binary operator. 'lexeme_next_on_same_line' is needed to identify function 
        names and unary left operators.

        Args:
            lexeme_prev:              The lexeme that comes directly before the current lexeme
            lexeme_current:           The lexeme to convert to a token
            lexeme_next:              The lexeme that comes directly after the current lexeme
            lexeme_next_on_same_line: True if the next lexeme is on the same line, else false.

        Returns
            None.
        """
        
        if not lexeme_current:
            return

        self.token_type: TokenType = TokenType.INVALID
        self.text: str = lexeme_current

        if rlexeme.is_keyword(lexeme_current):
            self.token_type = TokenType.KEY_WORD
        elif rlexeme.is_syntactic_name(lexeme_current):
            if lexeme_next == "(" and lexeme_next_on_same_line:
                self.token_type = TokenType.FUNCTION_NAME
            else:
                self.token_type = TokenType.SYNTACTIC_NAME
        elif rlexeme.is_comment(lexeme_current):
            self.token_type = TokenType.COMMENT
        elif rlexeme.is_constant_string(lexeme_current):
            self.token_type = TokenType.CONSTANT_STRING
        elif rlexeme.is_newline(lexeme_current):
            self.token_type = TokenType.NEW_LINE
        elif lexeme_current == ";":
            self.token_type = TokenType.END_STATEMENT
        elif lexeme_current == ",":
            self.token_type = TokenType.SEPARATOR
        elif rlexeme.is_sequence_of_spaces(lexeme_current):
            # sequence of spaces (needs to be after separator check, 
            #   else linefeed is recognised as space)
            self.token_type = TokenType.SPACE
        elif rlexeme.is_bracket(lexeme_current):
            if lexeme_current == "}":
                self.token_type = TokenType.END_SCRIPT
            else:
                self.token_type = TokenType.BRACKET
        elif rlexeme.is_operator_brackets(lexeme_current):
            self.token_type = TokenType.OPERATOR_BRACKET     # bracket operator     (e.g. '[')
        elif rlexeme.is_operator_unary(lexeme_current) \
                and (not lexeme_prev or not re.search('[a-zA-Z0-9_\\.)\\]]$', lexeme_prev)):
            self.token_type = TokenType.OPERATOR_UNARY_RIGHT # unary right operator (e.g. '!x')
        elif lexeme_current == "~" \
                and (not lexeme_next or not lexeme_next_on_same_line \
                     or not re.search('^[a-zA-Z0-9_\\.(\\+\\-\\!~]', lexeme_next)):
            self.token_type = TokenType.OPERATOR_UNARY_LEFT  # unary left operator  (e.g. x~)
        elif rlexeme.is_operator_reserved(lexeme_current) or re.search('^%%.*%%$', lexeme_current):
            self.token_type = TokenType.OPERATOR_BINARY      # 'binary operator     (e.g. '+')

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
        token = RToken(lexeme_prev, lexeme_current, lexeme_next, lexeme_next_on_same_line)

        """ Process key words
                Determine whether the next end statement will also be the end of the current script.
                Normally, a '}' indicates the end of the current script. However, R allows single
                statement scripts, not enclosed with '{}' for selected key words. 
                The key words that allow this are: if, else, while, for and function.
                For example:
                    if(x <= 0) y <- log(1+x) else y <- log(x)
        """
        if token.token_type == TokenType.COMMENT or token.token_type == TokenType.SPACE:
            # ignore comments and spaces (they don't affect key word processing)
            pass
        else:
            match token_state_stack[-1]:
                case TokenState.WAITING_FOR_OPEN_CONDITION:
                    if not token.token_type == TokenType.NEW_LINE and token.text == "(":
                        token_state_stack.pop()
                        token_state_stack.append(TokenState.WAITING_FOR_CLOSE_CONDITION)
                case TokenState.WAITING_FOR_CLOSE_CONDITION:
                    if num_open_brackets_stack[-1] == 0:
                        token_state_stack.pop()
                        token_state_stack.append(TokenState.WAITING_FOR_START_SCRIPT)
                case TokenState.WAITING_FOR_START_SCRIPT:
                    if not (token.token_type in (TokenType.COMMENT, TokenType.PRESENTATION, 
                                                 TokenType.SPACE, TokenType.NEW_LINE)):
                        token_state_stack.pop()
                        token_state_stack.append(TokenState.WAITING_FOR_END_SCRIPT)
                        if token.text == "{":
                            # script will terminate with '}'
                            is_script_enclosed_by_curly_brackets_stack.append(True)
                        else:
                            # script will terminate with end statement
                            is_script_enclosed_by_curly_brackets_stack.append(False)
                case TokenState.WAITING_FOR_END_SCRIPT:
                    """ 
                    a new line indicates the end of the statement when:
                        - statement contains at least one R element 
                            (i.e. not just spaces, comments, or newlines)
                        - there are no open brackets
                        - line doesn't end in a user-defined operator
                        - line doesn't end in a predefined operator, 
                            unless it's a tilda (the only operator that doesn't need a right-hand value)
                    """
                    if token.token_type == TokenType.NEW_LINE \
                            and statement_contains_element \
                            and num_open_brackets_stack[-1] == 0 \
                            and not rlexeme.is_operator_user_defined(lexeme_prev) \
                            and not rlexeme.is_operator_reserved(lexeme_prev) \
                            and not lexeme_prev == "~":
                        token.token_type = TokenType.END_STATEMENT
                        statement_contains_element = False
                    if token.token_type == TokenType.END_STATEMENT and is_script_enclosed_by_curly_brackets_stack[-1] == False and not lexeme_next:
                        token.token_type = TokenType.END_SCRIPT
                    if token.token_type == TokenType.END_SCRIPT:
                        is_script_enclosed_by_curly_brackets_stack.pop()
                        num_open_brackets_stack.pop()
                        token_state_stack.pop()
                case _:
                    raise Exception("The token is in an unknown state.")
        
        tokens.append(token)

        """
        If the script has ended and there are no more R elements to process, 
        then return the token list.
         
        Note: Any formatting lexemes (i.e. spaces, comments or extra newlines), after the 
        script's final statement, will not be added to the token list.
        For example, for the script below, '#comment1' will be added to the token list but 
        '#comment2' will not:
              
            a <- 1
            b <- a * 2 #comment1
            #comment2
                  
        This was a deliberate design decision. Spaces, comments or extra newlines at the end 
        of a script serve no practical purpose and are rarely used.
        However storing these extra formatting lexemes would increase source code complexity.
        """
        if token.token_type == TokenType.END_SCRIPT and not lexeme_next:
            return tokens
        pos += 1

    return tokens
