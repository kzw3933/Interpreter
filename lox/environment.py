from lox.token import Token
from lox.error import *


class Environment:
    def __init__(self, enclosing=None) -> None:
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise ErrorAtRuntime(name, f"Undefined variable '{name.lexeme}'.")
    
    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise ErrorAtRuntime(name, f"Undefined variable '{name.lexeme}'.")
    
    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    
    def assign_at(self, distance: int, name: Token, value: object) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def get_at(self, distance: int, name: Token) -> object:
        return self.ancestor(distance).values[name.lexeme]