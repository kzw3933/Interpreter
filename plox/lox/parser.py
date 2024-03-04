"""
句法文法
program     ->  declaration* EOF;
declaration ->  classDecl | funDecl | varDecl | statement;
classDecl   ->  "class" IDENTIFIER ("<" IDENTIFIER)? "{" function* "}";
funDecl     ->  "fun" function;
function    ->  IDENTIFIER "(" parameters? ")" block;
parameters  ->  IDENTIFIER ("," IDENTIFIERS)*;
varDecl     ->  "var" IDENTIFIER ("=" expression)? ";";
statement   ->  exprStmt | printStmt | block | forStmt | ifStmt | whileStmt | retrunStmt;
exprStmt    ->  expression ";";
printStmt   ->  "print" expression ";";
block       ->  "{" declaration* "}";
forStmt     ->  "for" "(" (varDecl | exprStmt | ";") expression? ";" expression? ";" statement;
ifStmt      ->  "if" "(" expression ")" statement ("else" statement)?;
whileStmt   ->  "while" "(" expression ")" statement; 
returnStmt  ->  "return" expression? ";"; 
expression  ->  assignment;
assignment  ->  (call ".")? IDENTIFIER "=" assignment | logic_or;
logic_or    ->  logic_and ("or" logic_and)*;
logic_and   ->  equality ("and" equality)*;
equality    ->  comparison ( ("!=" | "==) comparison)*;
comparison  ->  term ( (">" | ">=" | "<" | "<=") term)*;
term        ->  factor ( ("-" | "+") factor)*;
factor      ->  unary ( ("/" | "*") unary)*;
unary       ->  ( "!" | "-" ) unary | call;
call        ->  primary ("(" arguments? ")" | "." IDENTIFIER)*;
arguments   ->  expression ("," expression)*;
primary     ->  "true" | "false" | "nil" | "this" | NUMBER | STRING | "(" expression ")" | IDENTIFIER | "super" "." IDENTIFIER;
"""
from typing import List

import lox.expr as Expr
import lox.stmt as Stmt
from lox.error import *
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
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ErrorAtParse as e:
            self.synchronize()
            return None
        
    def class_declaration(self) -> Stmt.Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = Expr.Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods: List[Stmt.Function] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return Stmt.Class(name, superclass, methods)
    


    def function(self, kind: str) -> Stmt.Function:
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    error_handler.error_at_token(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before "+ kind + " body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

        
    def var_declaration(self) -> Stmt.Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)
    
    def statement(self) -> Stmt.Stmt:
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.block())
        return self.expression_statement()
    
    def for_statement(self) -> Stmt.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()

        if increment is not None:
            body = Stmt.Block(
                [body, Stmt.Expression(increment)]
            )
        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)
        if initializer is not None:
            body = Stmt.Block([
                initializer,
                body
            ])
        return body
    
    def while_statement(self) -> Stmt.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(condition, body)
    
    def if_statement(self) -> Stmt.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return Stmt.If(condition, then_branch, else_branch)

    
    def print_statement(self) -> Stmt.Stmt:
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(expression)
    
    def return_statement(self) -> Stmt.Stmt:
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)
    
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
        expr = self.or_expr()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                var: Expr.Variable = expr
                return Expr.Assign(var.name, value)
            elif isinstance(expr, Expr.Get):
                get: Expr.Get = expr
                return Expr.Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr
    
    def or_expr(self) -> Expr.Expr:
        expr = self.and_expr()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Expr.Logical(expr, operator, right)
        return expr
    
    def and_expr(self) -> Expr.Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
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
        return self.call()
    
    def call(self) -> Expr.Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER,"Expect property name after .")
                expr = Expr.Get(expr, name)
            else:
                break
        return expr
    
    def finish_call(self, callee: Expr.Expr) -> Expr.Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    error_handler.error_at_token(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)
    
    def primary(self) -> Expr.Expr:
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Expr.Super(keyword, method)
        if self.match(TokenType.THIS):
            return Expr.This(self.previous())
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
 