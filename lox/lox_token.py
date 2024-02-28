from dataclasses import dataclass

from token_type import TokenType

@dataclass(init=True, repr=True)
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

