from typing import List
from lox.callable import LoxCallable

import lox.stmt as Stmt
from lox.environment import Environment
from lox.error import *

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt.Function, closure: Environment, is_initializer: bool) -> None:
        self.declaration: Stmt.Function = declaration
        self.closure: Environment = closure
        self.is_initializer: bool = is_initializer

    def call(self, interpreter, arguments: List[object]) -> object:
        environment = Environment(self.closure)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_stmt:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_stmt.value
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)
    
    def __repr__(self) -> str:
        return f"<fn: {self.declaration.name.lexeme}>"


