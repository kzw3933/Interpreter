from abc import ABC, abstractmethod
from typing import List
from lox.token import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee: Expr = callee
        self.paren: Token = paren
        self.arguments: List[Expr] = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object: Expr = object
        self.name: Token = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value: object):
        self.value: object = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        self.object: Expr = object
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor):
        return visitor.visit_set_expr(self)

class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword: Token = keyword

    def accept(self, visitor):
        return visitor.visit_this_expr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Variable(Expr):
    def __init__(self, name: Token):
        self.name: Token = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


class Visitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: Assign):
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        pass

    @abstractmethod
    def visit_call_expr(self, expr: Call):
        pass

    @abstractmethod
    def visit_get_expr(self, expr: Get):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: Logical):
        pass

    @abstractmethod
    def visit_set_expr(self, expr: Set):
        pass

    @abstractmethod
    def visit_this_expr(self, expr: This):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: Variable):
        pass

