import sys
import os

sys.path.append(os.path.dirname(__file__))

from scanner import Scanner
from error import error_handler
from ast_printer import AstPrinter
from lox_parser import Parser

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
    expression = parser.parse()
    if(error_handler.had_error):
        return
    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
