from lox.expr import *
from lox.error import error_handler, ErrorAtRuntime
from lox.tokentype import TokenType
from lox.token import Token


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

class Interpreter(Visitor):
    def interpret(self, expression) -> None:
        try:
            value = self.evaluate(expression)
            print(value)
        except ErrorAtRuntime as e:
            error_handler.runtime_error(e)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value
    
    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Unary) -> object:
        value = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(value)
        elif expr.operator.type == TokenType.BANG:
            return not is_truthy(value)
        
        return None
    
    def visit_binary_expr(self, expr: Binary) -> object:
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

    def evaluate(self, expression) -> object:
        return expression.accept(self)
    
interpreter = Interpreter()