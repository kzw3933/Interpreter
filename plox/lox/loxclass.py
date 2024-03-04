from typing import Dict, List

from lox.callable import LoxCallable
from lox.loxfun import LoxFunction
from lox.loxinstance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass, methods: Dict[str, LoxFunction]) -> None:
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def __repr__(self) -> str:
        return self.name
    
    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()
    
    def call(self, interpreter, arguments: List[object]) -> object:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance
    
    def find_method(self, name: str) -> LoxFunction:
        if name in self.methods:
            return self.methods[name]
        elif self.superclass is not None:
            return self.superclass.find_method(name)
        return None