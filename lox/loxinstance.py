from typing import Dict

from lox.token import Token
from lox.loxfun import LoxFunction
from lox.error import ErrorAtRuntime

class LoxInstance:
    def __init__(self, kclass):
        self.kclass = kclass
        self.fields: Dict[str, object] = {}
        
    def __repr__(self) -> str:
        return self.kclass.name + " instancce"
    
    
    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method: LoxFunction = self.kclass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        raise ErrorAtRuntime(name, f"Undefined property '{name.lexeme}'.")
    
    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value
    
