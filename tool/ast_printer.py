import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import lox.expr as Expr
from lox.token import Token
from lox.tokentype import TokenType

class AstPrinter(Expr.Visitor):
    def visit_binary_expr(self, expr: Expr.Binary):
        return f"({expr.operator.lexeme} {' '.join([expr.accept(self) for expr in [expr.left, expr.right]])})"

    def visit_grouping_expr(self, expr: Expr.Grouping):
        return f"(grouping {expr.expression.accept(self)})"
    
    def visit_literal_expr(self, expr: Expr.Literal):
        return str(expr.value)
    
    def visit_unary_expr(self, expr: Expr.Unary):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"
    
    def visit_variable_expr(self, expr: Expr.Variable):
        return f"{expr.name}"
    
    def visit_assign_expr(self, expr: Expr.Assign):
        return f"(= {expr.name.accept(self)} {expr.value.accept(self)})"
    
    def visit_logical_expr(self, expr: Expr.Logical):
        return f"({expr.operator.lexeme} {' '.join([expr.accept(self) for expr in [expr.left, expr.right]])})"
    
    def visit_call_expr(self, expr: Expr.Call):
        return f"(call {expr.callee.accept(self)} {', '.join([argument.accept(self) for argument in expr.arguments])})"

    def print(self, expr: Expr.Expr):
        return expr.accept(self)
    
def main():
    expression = Expr.Binary(
        Expr.Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Expr.Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(
            Expr.Literal(45.67)
        )
    )
    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
