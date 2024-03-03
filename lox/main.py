import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lox.scanner import Scanner
from lox.parser import Parser

from lox.error import *
from lox.interpreter import interpreter
from lox.resolver import Resolver


def main():
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

def run_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        run(f.read())
    if error_handler.had_error:
        sys.exit(65)
    if error_handler.had_runtime_error:
        sys.exit(70)

def run_prompt():
    while True:
        line = input("> ")
        if line == '':
            break
        run(line)
        error_handler.had_error = False


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    statements = parser.parse()
    if error_handler.had_error:
        return
    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    if error_handler.had_error:
        return
    interpreter.interpret(statements)


if __name__ == "__main__":
    main()