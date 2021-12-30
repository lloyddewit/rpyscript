import re
from typing import List, Dict, Tuple
from relement import RElement
from relement_function import RElementFunction
from relement_operator import RElementOperator
from rparameter import RParameter
from rtoken import RToken, TokenType
import rtoken


class RStatement(object):

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

    def _get_tokens_presentation(self, tokens: List[RToken], pos: int) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        prefix = ''
        while pos < len(tokens):
            token: RToken = tokens[pos]
            pos += 1
            if token.token_type == TokenType.SPACE or token.token_type == TokenType.COMMENT or token.token_type == TokenType.NEW_LINE:
                prefix += token.text
            else:
                if prefix:
                    token.children.append(RToken(prefix, token_type = TokenType.PRESENTATION))
                tokens_new.append(token.clone_me())
                prefix = ''
        if prefix:
            token: RToken = RToken('', token_type = TokenType.END_STATEMENT)
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
            raise Exception('Token list ended unexpectedly.')
        return tokens[pos_tokens + 1].clone_me()

    def _get_tokens_operator_group(self, tokens: List[RToken], pos_operators: int) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

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
            if (token.text in RStatement._OPERATOR_PRECEDENCES[pos_operators] or \
                    pos_operators == RStatement._OPERATORS_USER_DEFINED and re.search('^%%.*%%$', token.text))  and \
                    (len(token.children) == 0 or \
                    (len(token.children) == 1 and token.children[0].token_type == TokenType.PRESENTATION)):
                match token.token_type:
                    case TokenType.OPERATOR_BRACKET if pos_operators == RStatement._OPERATORS_BRACKETS:
                        if not token_prev:
                            raise Exception('The bracket operator has no token on its left.')
                        
                        # make the previous and next tokens (up to the corresponding close bracket)
                        #   the children of the current token
                        token.children.append(token_prev.clone_me())
                        prev_token_processed = True
                        pos_tokens += 1
                        close_bracket: str = ']' if token.text == '[' else ']]'
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
                    case TokenType.OPERATOR_BINARY if pos_operators != RStatement._OPERATORS_UNARY_ONLY:
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
                            if token.token_type != token_next.token_type or token.text != token_next.text:
                                break
                            pos_tokens += 1
                            token.children.append(self._get_next_token(tokens, pos_tokens))
                            pos_tokens += 1

                    # edge case: if we found a unary '+' or '-', but we are not currently processing the unary '+'and '-' operators
                    case TokenType.OPERATOR_UNARY_RIGHT if not token.text in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_UNARY_ONLY] or pos_operators == RStatement._OPERATORS_UNARY_ONLY:
                        # make the next token, the child of the current operator token
                        token.children.append(self._get_next_token(tokens, pos_tokens))
                        pos_tokens += 1

                    case TokenType.OPERATOR_UNARY_LEFT:
                        if token_prev == None or pos_operators != RStatement._OPERATORS_TILDA:
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
            token.children = self._get_tokens_operator_group(token.clone_me().children, pos_operators)

            token_prev = token.clone_me()
            prev_token_processed = False
            pos_tokens += 1

        if token_prev == None:
            raise Exception('Expected that there would still be a token to add to the tree.')
        tokens_new.append(token_prev.clone_me())
        return tokens_new

    def _get_tokens_operators(self, tokens: List[RToken]) -> List[RToken]:
        if len(tokens) < 1:
            return List[RToken]()

        tokens_new: List[RToken] = List[RToken]()
        pos: int = 0
        while pos < len(RStatement._OPERATOR_PRECEDENCES):
            # restructure the tree for the next group of operators in the precedence list
            tokens_new = self._get_tokens_operator_group(tokens, pos)

            # clone the new tree before restructuring for the next operator
            tokens = List[RToken]()
            for token_temp in tokens_new:
                tokens.append(token_temp.clone_me())
            pos += 1
        return tokens_new

    def _get_child_pos_non_presentation(self, token: RToken) -> RToken:
        if not token:
            raise Exception("Cannot return a non-presentation child from an empty token.")
        
        for child in token.children:
            # if token is not a presentation token or a close bracket ')', then return the token
            if not child.token_type == TokenType.PRESENTATION \
                    and not (child.token_type == TokenType.BRACKET and child.text == ")"):
                return child
        raise Exception("Token must contain at least one non-presentation child.")

    def _get_parameter_named(self, token: RToken, assignments: Dict[str, RStatement]) -> RParameter | None:
        if not token:
            raise Exception('Cannot create a named parameter from an empty token.')

        match token.text:
            case '=':
                if len(token.children) < 2:
                    raise Exception(f'Named parameter token has {len(token.children)} children. ' + \
                                    'Named parameter must have at least 2 children ' + \
                                    '(plus an optional presentation child).')
                token_argument_name: RToken = token.children[len(token.children) - 2]
                parameter: RParameter = RParameter()
                parameter.arg_name = token_argument_name.text
                parameter.arg_val = self._get_element(token.children[len(token.children) - 1], assignments)
                """
                set the parameter's formatting prefix to the prefix of the parameter name.
                    Note: if the equals sign has any formatting information then this information 
                        will be lost.
                """
                parameter.prefix = token_argument_name.children[0].text \
                        if len(token_argument_name.children) > 0 \
                                and token_argument_name.children[0].token_type == TokenType.PRESENTATION \
                        else ''
                return parameter
            case ',':
                # if ',' is followed by a parameter name or value (e.g. 'fn(a,b)'), then return the parameter
                try:
                    return self._get_parameter_named(self._get_child_pos_non_presentation(token), assignments)
                except Exception as ex:
                    # return empty parameter (e.g. for cases like 'fn(a,)')
                    return RParameter()
            case ')':
                return None
            case _:
                parameter_named = RParameter()
                parameter_named.arg_val = self._get_element(token, assignments)
                parameter_named.prefix = token.children[0].text \
                        if len(token.children) > 0 and token.children[0].token_type == TokenType.PRESENTATION \
                        else ''
                return parameter_named

    def _get_element(self, token: RToken, assignments: Dict[str, RStatement], \
            bracketed_new: bool = False, package_name: str = '', \
            package_prefix: str = '', objects: List[RElement] | None = None) -> RElement | None:
        
        if not token:
            raise Exception('Cannot create an R element from an empty token.')

        match token.token_type:
            case TokenType.BRACKET:
                # if text is a round bracket, then return the bracket's child
                if token.text == '(':
                    if len(token.children) < 1 or len(token.children) > 3:
                        raise Exception(f'Open bracket token has {len(token.children)} ' \
                                'children. An open bracket must have exactly one child (plus an ' + \
                                'optional presentation child and/or an optional close bracket).')
                    
                    return self._get_element(self._get_child_pos_non_presentation(token), assignments, True)
                return RElement(token)

            case TokenType.FUNCTION_NAME:
                function: RElementFunction = RElementFunction(token, bracketed_new, package_name, package_prefix, objects)
                """  
                Note: Function tokens are structured as a tree.
                    For example 'f(a,b,c=d)' is structured as:
                    f
                    ..(
                    ....a
                    ....,
                    ......b 
                    ....,
                    ......=
                    ........c
                    ........d
                    ........)
                """                    
                if len(token.children) < 1 or len(token.children) > 2:
                    raise Exception(f'Function token has {len(token.children)} children. ' + \
                        'A function token must have 1 child (plus an optional presentation child).')

                # process each parameter
                bFirstParam: bool = True
                for token_param in token.children[len(token.children) - 1].children:
                    # if list item is a presentation element, then ignore it
                    if token_param.token_type == TokenType.PRESENTATION:
                        if bFirstParam:
                            continue                        
                        raise Exception('Function parameter list contained an unexpected presentation element.')                    

                    clsParameter: RParameter | None = self._get_parameter_named(token_param, assignments)
                    if clsParameter:
                        if bFirstParam and not clsParameter.arg_val:
                            function.parameters.append(clsParameter) # add extra empty parameter for case 'f(,)'
                        
                        function.parameters.append(clsParameter)
                    
                    bFirstParam = False
                return function

            case TokenType.OPERATOR_UNARY_LEFT:
                if len(token.children) < 1 or len(token.children) > 2:
                    raise Exception(f'Unary left operator token has {len(token.children)} children. ' + \
                            'A Unary left operator must have 1 child (plus an optional presentation child).')
                
                operator: RElementOperator = RElementOperator(token, bracketed_new)
                operator.parameters.append(self._get_parameter(token.children[len(token.children) - 1], assignments))
                return operator

            case TokenType.OPERATOR_UNARY_RIGHT:
                if len(token.children) < 1 or len(token.children) > 2:
                    raise Exception(f'Unary right operator token has {len(token.children)} children. ' + \
                            'A Unary right operator must have 1 child (plus an optional presentation child).')
                
                operator: RElementOperator(token, bracketed_new, True)
                operator.parameters.append(self._get_parameter(token.children[len(token.children) - 1], assignments))
                return operator

            case TokenType.OPERATOR_BINARY, TokenType.OPERATOR_BRACKET:
                if len(token.children) < 2:
                    raise Exception(f'Binary operator token has {len(token.children)} children. ' + \
                            'A binary operator must have at least 2 children (plus an optional presentation child).')
                
                # if object operator
                match token.text:
                    case '$':
                        package_prefix_new: str = ''
                        package_name_new: str = ''
                        objects_new: List[RElement] = []

                        # add each object parameter to the object list (except last parameter)
                        start_pos: int = 1 if token.children[0].token_type == TokenType.PRESENTATION else 0
                        pos: int = start_pos
                        while pos <= len(token.children) - 2:
                            token_object: RToken = token.children[pos]
                            pos += 1
                            # if the first parameter is a package operator ('::'), 
                            #   then make this the package name for the returned element
                            if pos == start_pos - 1 \
                                    and token_object.token_type == TokenType.OPERATOR_BINARY \
                                    and token_object.text == '::':
                                # get the package name and any package presentation information
                                package_name_new = self._get_token_package_name(token_object).text
                                package_prefix_new = self._get_package_prefix(token_object)
                                # get the object associated with the package, and add it to the object list
                                objects_new.append(self._get_element(
                                        token_object.children[len(token_object.children) - 1], assignments))
                                continue
                            objects_new.append(self._get_element(token_object, assignments))
                        
                        # the last item in the parameter list is the element we need to return
                        return self._get_element(token.children[len(token.children) - 1],
                                        assignments, bracketed_new, package_name_new,
                                        package_prefix_new, objects_new)

                    case '::':
                        # the '::' operator parameter list contains:
                        #  - the presentation string (optional)
                        #  - the package name
                        #  - the element associated with the package
                        return self._get_element(token.children[len(token.children) - 1],
                                        assignments, bracketed_new,
                                        self._get_token_package_name(token).text,
                                        self._get_package_prefix(token))

                    case _: # else if not an object or package operator, then add each parameter to the operator
                        operator: RElementOperator = RElementOperator(token, bracketed_new)
                        start_pos: int = 1 if token.children[0].token_type = TokenType.PRESENTATION else 0
                        pos: int = start_pos 
                        while pos <= len(token.children) - 1:
                            operator.parameters.append(self._get_parameter(token.children[pos], assignments))
                            pos += 1
                        return operator
                

            case TokenType.SYNTACTIC_NAME | TokenType.CONSTANT_STRING:
                # if element has a package name or object list, then return a property element
                if package_name or objects:
                    return RElementProperty(token, bracketed_new, package_name, package_prefix, objects)                

                # if element was assigned in a previous statement, then return an assigned element
                statement: RStatement | None = assignments.get(token.text)
                if statement:
                    return RElementAssignable(token, statement, bracketed_new)                

                # else just return a regular element
                return RElement(token, bracketed_new)

            case TokenType.PRESENTATION, TokenType.END_STATEMENT:
                # if token can't be used to generate an R element then ignore
                return None

            case _:
                raise Exception('The token has an unexpected type.')

    def __init__(self, tokens: List[RToken], pos: int, assignments: Dict[str, RStatement]) -> None:
        if len(tokens) < 1:
            return

        self.is_terminated_with_newline: bool = True
        self.assignment_operator: str = ''
        self.assignment_prefix: str = ''
        self.suffix: str = ''
        self.assignment: RElement | None = None
        self.element: RElement | None = None

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
            raise Exception('The token tree must contain at least one token.')

        if tokens_tree[0].token_type == TokenType.OPERATOR_BINARY and len(tokens_tree[0].children) > 1:

            token_child_left = tokens_tree[0].children[len(tokens_tree[0].children) - 2]
            token_child_right = tokens_tree[0].children[len(tokens_tree[0].children) - 1]

            if tokens_tree[0].text in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_LEFT_ASSIGNMENT1] or tokens_tree[0].text in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_LEFT_ASSIGNMENT2]:
                self.assignment = self._get_element(token_child_left, assignments)
                self.element = self._get_element(token_child_right, assignments)
            elif tokens_tree[0].text in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_RIGHT_ASSIGNMENT]:
                self.assignment = self._get_element(token_child_right, assignments)
                self.element = self._get_element(token_child_left, assignments)

        if self.assignment:
            self.assignment_operator = tokens_tree[0].text
            if tokens_tree[0].children[0].token_type == TokenType.PRESENTATION:
                self.assignment_prefix = tokens_tree[0].children[0].text
        else:
            self.element = self._get_element(tokens_tree[0], assignments)

        token_end_statement: RToken = tokens_tree[len(tokens_tree) - 1]
        if token_end_statement.token_type == TokenType.END_STATEMENT and token_end_statement.text == ';':
            self.is_terminated_with_newline = False

        if self.element == None and len(token_end_statement.children) > 0 and token_end_statement.children[0].token_type == TokenType.PRESENTATION:
            self.suffix = token_end_statement.children[0].text

    def get_as_executable_script(self) -> str:
        text: str = ''
        text_element: str = get_script_element(self.element)
        if not self.assignment or not self.assignment_operator:
            text = text_element
        else:
            text_assignment = get_script_element(self.assignment)
            if self.assignment_operator in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_LEFT_ASSIGNMENT1] or \
                    self.assignment_operator in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_LEFT_ASSIGNMENT2]:
                text = text_assignment + self.assignment_prefix + self.assignment_operator + text_element
            elif self.assignment_operator in RStatement._OPERATOR_PRECEDENCES[RStatement._OPERATORS_RIGHT_ASSIGNMENT]:
                text = text_element + self.assignment_prefix + self.assignment_operator + text_assignment
            else:
                raise Exception("The statement's assignment operator is an unknown type.")
        
        text += self.suffix + ('\n' if self.is_terminated_with_newline else ';')

        return text
