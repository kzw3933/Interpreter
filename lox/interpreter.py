from typing import List

import lox.expr as Expr
import lox.stmt as Stmt
from lox.error import *
from lox.tokentype import TokenType
from lox.token import Token
from lox.environment import Environment
from lox.lib import Clock
from lox.callable import LoxCallable
from lox.function import LoxFunction


def is_truthy(value: object):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return True

def is_equal(a: object, b: object):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a == b

def stringify(value: object) -> str:
    if value is None:
        return "nil"
    if isinstance(value, float):
        text = str(value)
        if text.endswith(".0"):
            text = text[:-2]
        return text
    return str(value)

def check_number_operand(operator: Token, operand: object):
    if isinstance(operand, float):
        return
    raise ErrorAtRuntime(operator, "Operand must be a number.")

def check_number_operands(operator: Token, left: object, right: object):
    if isinstance(left, float) and isinstance(right, float):
        return
    raise ErrorAtRuntime(operator, "Operands must be numbers.")

class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define(
            "clock",
            Clock()
        )

    def interpret(self, statements: List[Stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement) 
        except ErrorAtRuntime as e:
            error_handler.runtime_error(e)

    def visit_literal_expr(self, expr: Expr.Literal):
        return expr.value
    
    def visit_grouping_expr(self, expr: Expr.Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Expr.Unary):
        value = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(value)
        elif expr.operator.type == TokenType.BANG:
            return not is_truthy(value)
        
        return None
    
    def visit_binary_expr(self, expr: Expr.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.GREATER:
                check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return is_equal(left, right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise ErrorAtRuntime(expr.operator, "Operands must be two numbers or strings.")
            case TokenType.MINUS:
                check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.STAR:
                check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.SLASH:
                check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case _:
                return None
            
    def visit_variable_expr(self, expr: Expr.Variable):
        return self.environment.get(expr.name)
    
    def visit_assign_expr(self, expr: Expr.Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_logical_expr(self, expr: Expr.Logical):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if is_truthy(left):
                return left
        else:
            if not is_truthy(left):
                return left
        return self.evaluate(expr.right)
    
    def visit_call_expr(self, expr: Expr.Call):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxCallable):
            raise ErrorAtRuntime(expr.paren, "Can only call functions and classes.")
        function: LoxCallable = callee
        if len(arguments) != function.arity():
            raise ErrorAtRuntime(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)
    
    def visit_expression_stmt(self, stmt: Stmt.Expression):
        self.evaluate(stmt.expression)
    
    def visit_print_stmt(self, stmt: Stmt.Print):
        value = self.evaluate(stmt.expression)
        print(stringify(value))

    def visit_var_stmt(self, stmt: Stmt.Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt: Stmt.Block):
        self.execute_block(stmt.statements, Environment(self.environment))  

    def visit_if_stmt(self, stmt: Stmt.If) -> None:
        if is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None
    
    def visit_while_stmt(self, stmt: Stmt.While):
        while is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None
    
    def visit_function_stmt(self, stmt: Stmt.Function):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None
    
    def visit_return_stmt(self, stmt: Stmt.Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)


    def evaluate(self, expression: Expr.Expr) -> object:
        return expression.accept(self)
    
    def execute(self, statement: Stmt.Stmt) -> None:
        statement.accept(self)

    def execute_block(self, statements: List[Stmt.Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements: 
                self.execute(statement)
        finally:
            self.environment = previous
    
interpreter = Interpreter()