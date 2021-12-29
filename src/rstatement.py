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

    def get_tokens_operator_group(self, tokens: List[RToken], pos: int):
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        token_prev: RToken
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
            if ((((self.operator_precedences[pos].Contains(token.text) or ((((pos == intOperatorsUserDefined)) and Regex.IsMatch(token.text, "^%.*%$"))))) and ((((token.lstlen(tokens) == 0)) or ((((token.lstlen(tokens) == 1)) and ((token.lstTokens[0].enuToken == RToken.typToken.RPresentation)))))))):
                if ((token.enuToken == RToken.typToken.ROperatorBracket)):
                    if ((pos != intOperatorsBrackets)):
                    token.lstTokens.Add(token_prev.clone_me())
                    prev_token_processed = True
                    pos_tokens += 1
                    if ((token.text == "[")):
                        "]"
                        "]]"
                        iNumOpenBrackets = 1
                        while ((pos_tokens < len(tokens))):
                            ((tokens[pos_tokens].text == token.text))
                            1
                            0
                            ((tokens[pos_tokens].text == strCloseBracket))
                            1
                            0
                            if ((iNumOpenBrackets == 0)):
                            token.lstTokens.Add(tokens[pos_tokens].clone_me())
                            pos_tokens += 1
                        RToken.typToken.ROperatorBinary
                        if ((pos == intOperatorsUnaryOnly)):
                        elif ((clsTokenPrev == None)):
                            raise System.Exception("The binary operator has no parameter on its left.")
                        token.lstTokens.Add(token_prev.clone_me())
                        prev_token_processed = True
                        token.lstTokens.Add(GetNextToken(tokens, pos_tokens))
                        pos_tokens += 1
                        while ((pos_tokens < ((len(tokens) - 1)))):
                            clsTokenNext = GetNextToken(tokens, pos_tokens)
                            if (((not ((token.enuToken == clsTokenNext.enuToken))) or (not ((token.text == clsTokenNext.text))))):
                            pos_tokens += 1
                            token.lstTokens.Add(GetNextToken(tokens, pos_tokens))
                            pos_tokens += 1
                        RToken.typToken.ROperatorUnaryRight
                        if ((arrOperatorPrecedence(intOperatorsUnaryOnly).Contains(token.text) and (not ((pos == intOperatorsUnaryOnly))))):
                        token.lstTokens.Add(GetNextToken(tokens, pos_tokens))
                        pos_tokens += 1
                        RToken.typToken.ROperatorUnaryLeft
                        if ((((token_prev == None)) or (not ((pos == intOperatorsTilda))))):
                            raise System.Exception("Illegal unary left operator (\'~\' is the only valid unary left operator).")
                        token.lstTokens.Add(token_prev.clone_me())
                        prev_token_processed = True
                    else:
                        raise System.Exception("The token has an unknown operator type.")
            if (not prev_token_processed):
                if (not ((token_prev == None))):
                    tokens_new.Add(token_prev)
            token.lstTokens = GetLstTokenOperatorGroup(token.clone_me().lstTokens, pos)
            token_prev = token.clone_me()
            prev_token_processed = False
            pos_tokens += 1
        if ((token_prev == None)):
            raise System.Exception("Expected that there would still be a token to add to the tree.")
        tokens_new.Add(token_prev.clone_me())
        return tokens_new

    def get_tokens_operators(self, tokens: List[RToken]) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        pos: int = 0
        while pos < len(self.operator_precedences):
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

        self._OPERATORS_BRACKETS: int = 2
        self._OPERATORS_UNARY_ONLY: int = 4
        self._OPERATORS_USER_DEFINED: int = 6
        self._OPERATORS_TILDA: int = 13
        self._OPERATORS_RIGHT_ASSIGNMENT: int = 14
        self._OPERATORS_LEFT_ASSIGNMENT1: int = 15
        self._OPERATORS_LEFT_ASSIGNMENT2: int = 16

        self.operator_precedences = (('::', ':::'), ('$', '@'), ('[', '[['), ('^'), ('-', '+'), (':'), \
                                ('%'), ('*', '/'), ('+', '-'), ('<>', '<=', '>=', '==', '!='), \
                                ('!'), ('&', '&&'), ('|', '||'), ('~'), ('->', '->>'), \
                                ('<-', '<<-'), ('='))

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

            if tokens_tree[0].text in self.operator_precedences[self._OPERATORS_LEFT_ASSIGNMENT1] or tokens_tree[0].text in self.operator_precedences[self._OPERATORS_LEFT_ASSIGNMENT2]:
                self.assignment = get_element(token_child_left, assignments)
                self.element = get_element(token_child_right, assignments)
            elif tokens_tree[0].text in self.operator_precedences[self._OPERATORS_RIGHT_ASSIGNMENT]:
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
            if self.assignment_operator in self.operator_precedences[self._OPERATORS_LEFT_ASSIGNMENT1] or self.assignment_operator in self.operator_precedences[self._OPERATORS_LEFT_ASSIGNMENT2]:
                text = ((text_assignment + ((self.assignment_prefix + ((self.assignment_operator + text_element))))))
            elif self.assignment_operator in self.operator_precedences[self._OPERATORS_RIGHT_ASSIGNMENT]:
                text = ((text_element + ((self.assignment_prefix + ((self.assignment_operator + text_assignment))))))
            else:
                raise Exception("The statement's assignment operator is an unknown type.")
        
        text += self.suffix + ('\n' if self.is_terminated_with_newline else ';')

        return text
