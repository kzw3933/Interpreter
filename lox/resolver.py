from typing import List, Dict

import lox.expr as Expr
import lox.stmt as Stmt
from lox.types import FunctionType, ClassType
from lox.error import error_handler
from lox.token import Token
from lox.interpreter import Interpreter

class Resolver(Expr.Visitor, Stmt.Visitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: List[Dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def visit_variable_expr(self, expr: Expr.Variable):
        if len(self.scopes) > 0 and expr.name.lexeme in self.scopes[-1] and self.scopes[-1][expr.name.lexeme] is False:
            error_handler.error_at_token(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None

    def visit_assign_expr(self, expr: Expr.Assign):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    def visit_binary_expr(self, expr: Expr.Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_call_expr(self, expr: Expr.Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)
        return None
    
    def visit_grouping_expr(self, expr: Expr.Grouping):
        self.resolve(expr.expression)
        return None
    
    def visit_literal_expr(self, expr: Expr.Literal):
        return None
    
    def visit_logical_expr(self, expr: Expr.Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_unary_expr(self, expr: Expr.Unary):
        self.resolve(expr.right)
        return None
    
    def visit_get_expr(self, expr: Expr.Get):
        self.resolve(expr.object)
        return None
    
    def visit_set_expr(self, expr: Expr.Set):
        self.resolve(expr.object)
        self.resolve(expr.value)
        return None
    
    def visit_this_expr(self, expr: Expr.This):
        if self.current_class is ClassType.NONE:
            error_handler.error_at_token(expr.keyword, "Can't use 'this' outside of a class.")
            return None
        self.resolve_local(expr, expr.keyword)
        return None
    
    def visit_block_stmt(self, stmt: Stmt.Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None
    
    def visit_var_stmt(self, stmt: Stmt.Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_class_stmt(self, stmt: Stmt.Class):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        self.begin_scope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = FunctionType.INITIALIZER if method.name.lexeme == "init" else FunctionType.METHOD
            self.resolve_function(method, declaration)
        self.end_scope()
        self.current_class = enclosing_class
        return None

    
    def visit_function_stmt(self, stmt: Stmt.Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    def visit_expression_stmt(self, stmt: Stmt.Expression):
        self.resolve(stmt.expression)
        return None
    
    def visit_if_stmt(self, stmt: Stmt.If):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt: Stmt.Print):
        self.resolve(stmt.expression)
        return None
    
    def visit_return_stmt(self, stmt: Stmt.Return):
        if self.current_function is FunctionType.NONE:
            error_handler.error_at_token(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function is FunctionType.INITIALIZER:
                error_handler.error_at_token(stmt.keyword, "Can't return a value from an initializer.")
            self.resolve(stmt.value)
        return None
    
    def visit_while_stmt(self, stmt: Stmt.While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()


    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            error_handler.error_at_token(name, "Already variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr.Expr, name: Token):
        for distance, scope in enumerate(self.scopes[::-1]):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, distance)
                return
            
    def resolve_function(self, function: Stmt.Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def resolve(self, expr: Expr.Expr | Stmt.Stmt | List[Stmt.Stmt]):
        if isinstance(expr, list):
            stmts = expr
            for stmt in stmts:
                self.resolve(stmt)
        else:
            expr.accept(self)


    

    



        