from typing import List
from rtoken import RToken
from relement import RElement
from relement_property import RElementProperty
from rparameter import RParameter

class RElementFunction(RElementProperty):
    def __init__(self, token: RToken, is_bracketed: bool = False, package_name: str = '', package_prefix: str = '', objects: List[RElement] | None = None):
        
        self.parameters: List[RParameter] = []
        super(RElementFunction, self).__init__(token, objects, is_bracketed, package_name, package_prefix)
