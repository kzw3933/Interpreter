import sys
import os

sys.path.append(os.path.dirname(__file__))

from scanner import Scanner
from errorhandler import error_handler

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
        sys.stdout.write("> ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if line == '':
            break
        run(line)
        error_handler.had_error = False


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
