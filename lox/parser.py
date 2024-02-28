"""
句法文法
program     ->  declaration* EOF;
declaration ->  varDecl | statement;
varDecl     ->  "var" IDENTIFIER ("=" expression)? ";";
statement   ->  exprStmt | printStmt | block;
exprStmt    ->  expression ";";
printStmt   ->  "print" expression ";";
block       ->  "{" declaration* "}";
expression  ->  assignment;
assignment  ->  IDENTIFIER "=" assignment | equality;
equality    ->  comparison ( ("!=" | "==) comparison)*;
comparison  ->  term ( (">" | ">=" | "<" | "<=") term)*;
term        ->  factor ( ("-" | "+") factor)*;
factor      ->  unary ( ("/" | "*") unary)*;
unary       ->  ( "!" | "-" ) unary | primary;
primary     ->  "true" | "false" | "nil" | NUMBER | STRING | "(" expression ")" | IDENTIFIER;
"""
from typing import List

import lox.expr as Expr
import lox.stmt as Stmt
from lox.error import error_handler, ErrorAtParse
from lox.tokentype import TokenType
from lox.token import Token

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt.Stmt]:

        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements
    
    def declaration(self) -> Stmt.Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ErrorAtParse as e:
            self.synchronize()
            return None
        
    def var_declaration(self) -> Stmt.Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)
    
    def statement(self) -> Stmt.Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.block())
        return self.expression_statement()
    
    def print_statement(self) -> Stmt.Stmt:
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(expression)
    
    def expression_statement(self) -> Stmt.Stmt:
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Expression(expression)
    
    def block(self) -> List[Stmt.Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
            
    def expression(self) -> Expr.Expr:
        return self.assignment()
    
    def assignment(self) -> Expr.Expr:
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr
    
    def equality(self) -> Expr.Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr
    

    def comparison(self) -> Expr.Expr:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expr.Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr.Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()
    
    def primary(self) -> Expr.Expr:
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")
    

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def check(self, type: TokenType) -> bool:
        return not self.is_at_end() and self.peek().type == type 
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def error(self, token, message):
        error_handler.error_at_token(token, message)
        return ErrorAtParse()

    def synchronize(self) -> None:
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return
            
            self.advance()
 