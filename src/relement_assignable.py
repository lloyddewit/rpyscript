from relement import RElement
from rstatement import RStatement
from rtoken import RToken

class RElementAssignable(RElement):
    def __init__(self, token: RToken, statement: RStatement | None, is_bracketed: bool = False, package_prefix: str = "") -> None:
        super(RElementAssignable, self).__init__(token, is_bracketed, package_prefix)
        self.statement: RStatement | None = statement
