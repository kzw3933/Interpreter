from abc import ABC, abstractmethod
from typing import List
from lox.token import Token
import lox.expr as Expr

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements: List[Stmt] = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class Function(Stmt):
    def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
        self.name: Token = name
        self.params: List[Token] = params
        self.body: List[Stmt] = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)

class Class(Stmt):
    def __init__(self, name: Token, superclass: Expr.Variable, methods: List[Function]):
        self.name: Token = name
        self.superclass: Expr.Variable = superclass
        self.methods: List[Function] = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)

class Expression(Stmt):
    def __init__(self, expression: Expr.Expr):
        self.expression: Expr.Expr = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr.Expr):
        self.expression: Expr.Expr = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class If(Stmt):
    def __init__(self, condition: Expr.Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition: Expr.Expr = condition
        self.then_branch: Stmt = then_branch
        self.else_branch: Stmt = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    def __init__(self, condition: Expr.Expr, body: Stmt):
        self.condition: Expr.Expr = condition
        self.body: Stmt = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr.Expr):
        self.name: Token = name
        self.initializer: Expr.Expr = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr.Expr):
        self.keyword: Token = keyword
        self.value: Expr.Expr = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class Visitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Block):
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt: Function):
        pass

    @abstractmethod
    def visit_class_stmt(self, stmt: Class):
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: If):
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: While):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Var):
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt: Return):
        pass

