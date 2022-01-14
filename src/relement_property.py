from typing import List
from relement_assignable import RElementAssignable
from rtoken import RToken, TokenType
from relement import RElement

class RElementProperty(RElementAssignable):
    def __init__(self, token: RToken, objects: List[RElement] | None, is_bracketed: bool = False, package_name: str = "", package_prefix: str = "") -> None:
        super(RElementProperty, self).__init__(self.get_token_clean(token, objects, package_name), None, is_bracketed, package_prefix)
        
        # package_name and objects are only used for functions and variables (e.g. 'constants::syms$h')
        self.package_name: str = package_name   
        self.objects: List[RElement] | None= objects  
    
    def get_token_clean(self, token: RToken, objects: List[RElement] | None, package_name: str = "") -> RToken:
        clsTokenNew = token.clone_me()
        # Edge case: if the object has a package name or an object list, and formatting information
        if (package_name or (objects and len(objects) > 0)) and (len(token.children) > 0 and token.children[0].token_type == TokenType.PRESENTATION):
            """
            remove any formatting information associated with the main element.
                This is needed to pass test cases such as:
                pkg ::  obj1 $ obj2$ fn1 ()' should be displayed as 'pkg::obj1$obj2$fn1()' 
            """
            clsTokenNew.children[0].text = ""
        return clsTokenNew
