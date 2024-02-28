import sys

from lox.tokentype import TokenType
from lox.token import Token

class ErrorAtParse(Exception):
    pass

class ErrorAtRuntime(Exception):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token
class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error_at_line(self, line, message) -> None:
        self.report(line, "", message)

    def error_at_token(self, token, message) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)

    def runtime_error(self, error: ErrorAtRuntime) -> None:
        print(f"[line {error.token.line}] {error}")
        self.had_runtime_error = True

    def report(self, line, where, message) -> None:
        sys.stderr.write(
            f"[line {line}] Error {where}: {message}"
        )
        sys.stderr.write('\n')
        sys.stderr.flush()
        self.had_error = True

error_handler = ErrorHandler()