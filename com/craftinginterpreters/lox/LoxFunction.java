package com.craftinginterpreters.lox;

import java.util.List;

public class LoxFunction implements LoxCallable {
    private final Stmt.Function declaraton;
    private final Environment closure;
    LoxFunction(Stmt.Function declaration, Environment closure) {
        this.declaraton = declaration;
        this.closure = closure;
    }

    @Override
    public Object call(Interpreter interpreter, List<Object> arguments) {
        Environment environment = new Environment(closure);
        for(int i=0; i < declaraton.params.size(); i++) {
            environment.define(declaraton.params.get(i).lexeme,
                    arguments.get(i));
        }

        try {
            interpreter.executeBlock(declaraton.body, environment);
        } catch (Return returnValue) {
            return returnValue.value;
        }

        return null;
    }

    @Override
    public int arity() {
        return declaraton.params.size();
    }

    @Override
    public String toString() {
        return "<fn "+ declaraton.name.lexeme + ">";
    }
}
