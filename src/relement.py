from rtoken import RToken, TokenType

class RElement(object):
    def __init__(self, token: RToken, is_bracketed: bool = False, package_prefix: str = "") -> None:
        self.text: str = token.text
        self.is_bracketed = is_bracketed
        self.prefix: str = package_prefix
        if len(token.children) > 0 and token.children[0].token_type == TokenType.PRESENTATION:
            self.prefix += token.children[0].text
