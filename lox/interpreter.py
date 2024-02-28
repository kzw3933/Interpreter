from typing import List

import lox.expr as Expr
import lox.stmt as Stmt
from lox.error import error_handler, ErrorAtRuntime
from lox.tokentype import TokenType
from lox.token import Token
from lox.environment import Environment


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
        self.environment = Environment()

    def interpret(self, statements: List[Stmt.Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement) 
        except ErrorAtRuntime as e:
            error_handler.runtime_error(e)

    def visit_literal_expr(self, expr: Expr.Literal) -> object:
        return expr.value
    
    def visit_grouping_expr(self, expr: Expr.Grouping) -> object:
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Expr.Unary) -> object:
        value = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(value)
        elif expr.operator.type == TokenType.BANG:
            return not is_truthy(value)
        
        return None
    
    def visit_binary_expr(self, expr: Expr.Binary) -> object:
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
            
    def visit_variable_expr(self, expr: Expr.Variable) -> object:
        return self.environment.get(expr.name)
    
    def visit_assign_expr(self, expr: Expr.Assign) -> object:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_expression_stmt(self, stmt: Stmt.Expression) -> None:
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