import re
from typing import List, Dict, Tuple
from relement import RElement
from rtoken import RToken, TokenType


class RStatement(object):

    def _get_tokens_presentation(self, tokens: List[RToken], pos: int) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        prefix = ""
        while pos < len(tokens):
            token: RToken = tokens[pos]
            pos += 1
            if token.token_type == TokenType.SPACE or token.token_type == TokenType.COMMENT or token.token_type == TokenType.NEW_LINE:
                prefix += token.text
            else:
                if prefix:
                    token.children.append(RToken(prefix, token_type = TokenType.PRESENTATION))
                tokens_new.append(token.clone_me())
                prefix = ""
        if prefix:
            token: RToken = RToken("", token_type = TokenType.END_STATEMENT)
            token.children.append(RToken(prefix, token_type = TokenType.PRESENTATION))
            tokens_new.append(token)
        return tokens_new

    def _get_tokens_brackets(self, tokens: List[RToken], pos: int) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        while pos < len(tokens):
            token: RToken = tokens[pos]
            pos += 1
            match token.text:
                case '(':
                    tokens_temp: List[RToken] = self._get_tokens_brackets(tokens, pos)
                    for token_child in tokens_temp:
                        if not token_child:
                            raise Exception('Token has illegal empty child.')
                        token.children.append(token_child.clone_me())
                case ')':
                    tokens_new.append(token.clone_me())
                    return tokens_new
            tokens_new.append(token.clone_me())
        return tokens_new
    
    def _get_tokens_function_brackets(self, tokens: List[RToken]) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        pos: int = 0
        while pos < len(tokens):
            token: RToken = tokens[pos]
            if token.token_type == TokenType.FUNCTION_NAME:
                if pos > len(tokens) - 2:
                    raise Exception("The function's parameters have an unexpected format and cannot be processed.")
                # make the function's open bracket a child of the function name
                pos += 1
                token.children.append(tokens[pos].clone_me())
            tokens = self._get_tokens_function_brackets(token.clone_me().children)
            tokens.append(token.clone_me())
            pos += 1
        return tokens_new

    def _get_tokens_commas(self, tokens: List[RToken], pos: int, processing_comma: bool = False) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        while pos < len(tokens):
            token: RToken = tokens[pos]
            match token.text:
                case ',':
                    if processing_comma:
                        pos -= 1 #ensure this comma is processed in the level above
                        return tokens_new
                    pos += 1
                    token.children += self._get_tokens_commas(tokens, pos, True)
                case ')':
                    tokens.append(token)
                    return tokens_new
                case _:
                    if len(token.children) > 0:
                        token.children = self._get_tokens_commas(token.clone_me().children, 0)
            tokens_new.append(token)
            pos += 1
        return tokens_new

    def _get_next_token(self, tokens: List[RToken], pos_tokens: int) -> RToken:
        if pos_tokens >= len(tokens) - 1:
            raise Exception("Token list ended unexpectedly.")
        return tokens[pos_tokens + 1].clone_me()

    def get_tokens_operator_group(self, tokens: List[RToken], pos_operators: int) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        _OPERATORS_BRACKETS: int = 2
        _OPERATORS_UNARY_ONLY: int = 4
        _OPERATORS_USER_DEFINED: int = 6
        _OPERATORS_TILDA: int = 13
        _OPERATORS_RIGHT_ASSIGNMENT: int = 14
        _OPERATORS_LEFT_ASSIGNMENT1: int = 15
        _OPERATORS_LEFT_ASSIGNMENT2: int = 16

        _OPERATOR_PRECEDENCES = (('::', ':::'), ('$', '@'), ('[', '[['), ('^'), ('-', '+'), (':'), \
                                ('%'), ('*', '/'), ('+', '-'), ('<>', '<=', '>=', '==', '!='), \
                                ('!'), ('&', '&&'), ('|', '||'), ('~'), ('->', '->>'), \
                                ('<-', '<<-'), ('='))

        tokens_new: List[RToken] = List[RToken]()
        token_prev: RToken | None = None
        prev_token_processed: bool = False

        pos_tokens: int = 0
        while pos_tokens < len(tokens):
            token: RToken = tokens[pos_tokens].clone_me()

            """
            if the token is the operator we are looking for and it has not been processed already
            Edge case: if the operator already has (non-presentation) children then it means 
                       that it has already been processed. This happens when the child is in the 
                       same precedence group as the parent but was processed first in accordance 
                       with the left to right rule (e.g. 'a/b*c').
            """
            if (token.text in _OPERATOR_PRECEDENCES[pos_operators] or \
                    pos_operators == _OPERATORS_USER_DEFINED and re.search('^^%%.*%%$', token.text))  and \
                    (len(token.children) == 0 or \
                    (len(token.children) == 1 and token.children[0].token_type == TokenType.PRESENTATION)):
                match token.token_type:
                    case TokenType.OPERATOR_BRACKET if pos_operators == _OPERATORS_BRACKETS:
                        if not token_prev:
                            raise Exception('The bracket operator has no token on its left.')
                        
                        # make the previous and next tokens (up to the corresponding close bracket)
                        #   the children of the current token
                        token.children.append(token_prev.clone_me())
                        prev_token_processed = True
                        pos_tokens += 1
                        close_bracket: str = ']' if token.text == '[' else 
                        num_open_brackets = 1
                        while pos_tokens < len(tokens):
                            num_open_brackets += 1 if tokens[pos_tokens].text == token.text else 0
                            num_open_brackets -= 1 if tokens[pos_tokens].text == close_bracket else 0
                            if num_open_brackets == 0:
                                break # discard the terminating close bracket
                            token.children.append(tokens[pos_tokens].clone_me())
                            pos_tokens += 1

                    # edge case: if we are looking for unary '+' or '-' and we found a binary '+' or '-',
                    #   then do not process (binary '+' and '-' have a lower precedence and will be processed later)
                    case TokenType.OPERATOR_BINARY if pos_operators != _OPERATORS_UNARY_ONLY:
                        if not token_prev:
                            raise Exception('The binary operator has no token on its left.')

                        # make the previous and next tokens, the children of the current token
                        token.children.append(token_prev.clone_me())
                        prev_token_processed = True
                        token.children.append(self._get_next_token(tokens, pos_tokens))
                        pos_tokens += 1

                        # while next token is the same operator (e.g. 'a+b+c+d...'), 
                        #   then keep making the next token, the child of the current operator token
                        while pos_tokens < len(tokens) - 1:
                            token_next: RToken | None = self._get_next_token(tokens, pos_tokens)
                            if token.token_type != token_next.token_type or token.text != token_next.text):
                                break
                            pos_tokens += 1
                            token.children.append(self._get_next_token(tokens, pos_tokens))
                            pos_tokens += 1

                    # edge case: if we found a unary '+' or '-', but we are not currently processing the unary '+'and '-' operators
                    case TokenType.OPERATOR_UNARY_RIGHT if not token.text in _OPERATOR_PRECEDENCES[_OPERATORS_UNARY_ONLY] or pos_operators == _OPERATORS_UNARY_ONLY:
                        # make the next token, the child of the current operator token
                        token.children.append(self._get_next_token(tokens, pos_tokens))
                        pos_tokens += 1

                    case TokenType.OPERATOR_UNARY_LEFT:
                        if token_prev == None or pos_operators != _OPERATORS_TILDA:
                            raise Exception("Illegal unary left operator ('~' is the only valid unary left operator).")
                        
                        # make the previous token, the child of the current operator token
                        token.children.append(token_prev.clone_me())
                        prev_token_processed = True

            # if token was not the operator we were looking for
            #   (or we were looking for a unary right operator)
            if not prev_token_processed and token_prev:
                # add the previous token to the tree
                tokens_new.append(token_prev)

            # process the current token's children
            token.children = self.get_tokens_operator_group(token.clone_me().children, pos_operators)

            token_prev = token.clone_me()
            prev_token_processed = False
            pos_tokens += 1

        if token_prev == None:
            raise Exception("Expected that there would still be a token to add to the tree.")
        tokens_new.append(token_prev.clone_me())
        return tokens_new

    def get_tokens_operators(self, tokens: List[RToken]) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        pos: int = 0
        while pos < len(_OPERATOR_PRECEDENCES):
            # restructure the tree for the next group of operators in the precedence list
            tokens_new = get_tokens_operator_group(tokens, pos)

            # clone the new tree before restructuring for the next operator
            tokens = List[RToken]()
            for token_temp in tokens_new:
                tokens.append(token_temp.clone_me())
            pos += 1
        return tokens_new

    def __init__(self, tokens: List[RToken], pos: int, assignments: Dict[str, RStatement]) -> None:
        if len(tokens) < 1:
            return

        self.is_terminated_with_newline: bool = True
        self.assignment_operator: str = ""
        self.assignment_prefix: str = ""
        self.suffix: str = ""
        self.assignment: RElement
        self.element: RElement

        statement_tokens: List[RToken] = []
        while pos < len(tokens):
            statement_tokens.append(tokens[pos])
            if tokens[pos].token_type == TokenType.END_STATEMENT or tokens[pos].token_type == TokenType.END_SCRIPT:
                pos += 1
                break
            pos += 1
        
        tokens_presentation: List[RToken] = self._get_tokens_presentation(statement_tokens, 0)
        tokens_brackets: List[RToken] = self._get_tokens_brackets(tokens_presentation, 0)
        tokens_function_brackets: List[RToken] = self._get_tokens_function_brackets(tokens_brackets)
        tokens_commas: List[RToken] = self._get_tokens_commas(tokens_function_brackets, 0)
        tokens_tree: List[RToken] = self._get_tokens_operators(tokens_commas)

        if len(tokens_tree) < 1:
            raise Exception("The token tree must contain at least one token.")

        if tokens_tree[0].token_type == TokenType.OPERATOR_BINARY and len(tokens_tree[0].children) > 1:

            token_child_left = tokens_tree[0].children[len(tokens_tree[0].children) - 2]
            token_child_right = tokens_tree[0].children[len(tokens_tree[0].children) - 1]

            if tokens_tree[0].text in _OPERATOR_PRECEDENCES[_OPERATORS_LEFT_ASSIGNMENT1] or tokens_tree[0].text in _OPERATOR_PRECEDENCES[_OPERATORS_LEFT_ASSIGNMENT2]:
                self.assignment = get_element(token_child_left, assignments)
                self.element = get_element(token_child_right, assignments)
            elif tokens_tree[0].text in _OPERATOR_PRECEDENCES[_OPERATORS_RIGHT_ASSIGNMENT]:
                self.assignment = get_element(token_child_right, assignments)
                self.element = get_element(token_child_left, assignments)

        if self.assignment:
            self.assignment_operator = tokens_tree[0].text
            if tokens_tree[0].children[0].token_type == TokenType.PRESENTATION:
                self.assignment_prefix = tokens_tree[0].children[0].text
        else:
            self.element = get_element(tokens_tree[0], assignments)

        token_end_statement: RToken = tokens_tree[len(tokens_tree) - 1]
        if token_end_statement.token_type == TokenType.END_STATEMENT and token_end_statement.text == ";":
            self.is_terminated_with_newline = False

        if self.element == None and len(token_end_statement.children) > 0 and token_end_statement.children[0].token_type == TokenType.PRESENTATION:
            self.suffix = token_end_statement.children[0].text

    def get_as_executable_script(self) -> str:
        text: str = ""
        text_element: str = get_script_element(self.element)
        if not self.assignment or not self.assignment_operator:
            text = text_element
        else:
            text_assignment = get_script_element(self.assignment)
            if self.assignment_operator in _OPERATOR_PRECEDENCES[_OPERATORS_LEFT_ASSIGNMENT1] or \
                    self.assignment_operator in _OPERATOR_PRECEDENCES[_OPERATORS_LEFT_ASSIGNMENT2]:
                text = text_assignment + self.assignment_prefix + self.assignment_operator + text_element
            elif self.assignment_operator in _OPERATOR_PRECEDENCES[_OPERATORS_RIGHT_ASSIGNMENT]:
                text = text_element + self.assignment_prefix + self.assignment_operator + text_assignment
            else:
                raise Exception("The statement's assignment operator is an unknown type.")
        
        text += self.suffix + ('\n' if self.is_terminated_with_newline else ';')

        return text
