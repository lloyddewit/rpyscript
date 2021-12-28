from relement import RElement

class RParameter(object):
    def __init__(self) -> None:
        self.arg_name: str = ""
        self.arg_val: RElement 
        self.arg_val_default: RElement
        self.arg_pos: int = 0
        self.arg_pos_definition: int = 0
        self.strPrefix: str = ""
