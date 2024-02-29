from typing import List
from lox.callable import LoxCallable

import lox.stmt as Stmt
from lox.environment import Environment
from lox.error import *

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt.Function, closure: Environment) -> None:
        self.declaration: Stmt.Function = declaration
        self.closure: Environment = closure

    def call(self, interpreter, arguments: List[object]) -> object:
        environment = Environment(self.closure)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_stmt:
            return return_stmt.value

        return None

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __repr__(self) -> str:
        return f"<fn: {self.declaration.name.lexeme}>"


