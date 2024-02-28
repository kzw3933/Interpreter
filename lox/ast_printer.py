import sys
import os

sys.path.append(os.path.dirname(__file__))

from expr import *
from lox_token import Token
from token_type import TokenType

class AstPrinter(Visitor):
    def visit_binary_expr(self, expr):
        return f"({expr.operator.lexeme} {' '.join([expr.accept(self) for expr in [expr.left, expr.right]])})"

    def visit_grouping_expr(self, expr):
        return f"(grouping {expr.expression.accept(self)})"
    
    def visit_literal_expr(self, expr):
        return str(expr.value)
    
    def visit_unary_expr(self, expr):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"
    
    def print(self, expr):
        return expr.accept(self)
    
def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )
    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
