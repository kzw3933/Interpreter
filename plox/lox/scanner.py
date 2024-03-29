from typing import List, Optional

from lox.tokentype import TokenType
from lox.token import Token
from lox.error import *

def is_alpha(c):
    return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'

def is_digit(c):
    return c >= '0' and c <= '9'

def is_alpha_digit(c):
    return is_alpha(c) or is_digit(c)

class Scanner:
    keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens
    
    def scan_token(self) -> None:
        c: str = self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ':
                pass
            case '\r':
                pass
            case '\t': 
                pass
            case '\n': self.line += 1
            case '"': self.string()
            case _:
                if is_digit(c):
                    self.number()
                elif is_alpha(c):
                    self.identifier()
                else:
                    error_handler.error_at_line(self.line, "Unexpected character.")

    def identifier(self) -> None:
        while is_alpha_digit(self.peek()):
            self.advance()
        text: str = self.source[self.start:self.current]
        type: TokenType = Scanner.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)

    def number(self) -> None:
        while is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and is_digit(self.peek_next()):
            self.advance()
            while is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            error_handler.error_at_line(self.line, "Unterminated string.")
            return
        
        self.advance()

        value: str = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    
    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peek(self) -> str:
        return self.source[self.current] if not self.is_at_end() else '\0'
    
    def peek_next(self) -> str:
        return self.source[self.current + 1] if self.current + 1 < len(self.source) else '\0'
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def advance(self) -> str:
        self.current += 1
        return self.source[self.current-1]
    
    def add_token(self, type: TokenType, literal: Optional[object] = None) -> None:
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    

    

