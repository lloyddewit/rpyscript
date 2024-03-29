from relement import RElement
from rtoken import RToken

class RElementAssignable(RElement):
    def __init__(self, token: RToken, statement, is_bracketed: bool = False, package_prefix: str = "") -> None:
        super(RElementAssignable, self).__init__(token, is_bracketed, package_prefix)
        import rstatement
        self.statement: rstatement.RStatement | None = statement
