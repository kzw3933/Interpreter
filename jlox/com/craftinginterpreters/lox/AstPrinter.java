package com.craftinginterpreters.lox;

public class AstPrinter implements Expr.Visitor<String> {
    String print(Expr expr) {
        return expr.accept(this);
    }

    @Override
    public String visitBinaryExpr(Expr.Binary expr) {
        return parenthesize(expr.operator.lexeme, expr.left, expr.right);
    }

    @Override
    public String visitGroupingExpr(Expr.Grouping expr) {
        return parenthesize("group", expr.expression);
    }

    @Override
    public String visitLiteralExpr(Expr.Literal expr) {
        if(expr.value == null) return "nil";
        return expr.value.toString();
    }

    @Override
    public String visitUnaryExpr(Expr.Unary expr) {
        return parenthesize(expr.operator.lexeme, expr.right);
    }

    @Override 
    public String visitVariableExpr(Expr.Variable expr) {
        return expr.name.lexeme;
    }

    @Override 
    public String visitAssignExpr(Expr.Assign expr) {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append("=");
        builder.append(" ").append(expr.name.lexeme);
        builder.append(" ").append(expr.value.accept(this));
        builder.append(")");
        return builder.toString();
    }

    @Override
    public String visitLogicalExpr(Expr.Logical expr) {
        return parenthesize(expr.operator.lexeme, expr.left, expr.right);
    }

    @Override
    public String visitCallExpr(Expr.Call expr) {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append("call");
        builder.append(" ").append(expr.callee.accept(this));
        for(Expr arg: expr.arguments) {
            builder.append(" ");
            builder.append(arg.accept(this));
        }
        builder.append(")");
        return builder.toString();
    }

    @Override
    public String visitGetExpr(Expr.Get expr) {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append("get");
        builder.append(" ").append(expr.object.accept(this));
        builder.append(" ").append(expr.name.lexeme);
        builder.append(")");
        return builder.toString();
    }

    @Override
    public String visitSetExpr(Expr.Set expr) {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append("set");
        builder.append(" ").append(expr.object.accept(this));
        builder.append(" ").append(expr.name.lexeme);
        builder.append(")");
        return builder.toString();
    }

    @Override 
    public String visitThisExpr(Expr.This expr) {
        return "this";
    }

    @Override 
    public String visitSuperExpr(Expr.Super expr) {
        return "super";
    }

    private String parenthesize(String name, Expr... exprs) {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append(name);
        for(Expr expr: exprs) {
            builder.append(" ");
            builder.append(expr.accept(this));
        }
        builder.append(")");
        return builder.toString();
    }

    public static void main(String[] args) {
        Expr expression = new Expr.Binary(
            new Expr.Unary(
                new Token(TokenType.MINUS, "-", null, 1),
                new Expr.Literal(123)),
            new Token(TokenType.STAR, "*", null, 1),
            new Expr.Grouping(
                new Expr.Literal(45.67)));
    
        System.out.println(new AstPrinter().print(expression));
    }

}
