from dataclasses import dataclass

from tokentype import TokenType

@dataclass(init=True, repr=True)
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

