from lox.token import Token
from lox.error import ErrorAtRuntime


class Environment:
    def __init__(self, enclosing=None) -> None:
        self.enclosing = enclosing
        self.values = dict()

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
