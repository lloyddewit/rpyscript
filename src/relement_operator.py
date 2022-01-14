from typing import List
from rparameter import RParameter
from relement_assignable import RElementAssignable
from rtoken import RToken

class RElementOperator(RElementAssignable):
    def __init__(self, token: RToken, bracketed_new: bool = False, first_param_on_right_new: bool = False):
        super(RElementOperator, self).__init__(token, None, bracketed_new)
        self.terminator = ""
        self.parameters: List[RParameter] = []
        self.first_param_on_right = first_param_on_right_new
