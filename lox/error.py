import sys
from token_type import TokenType

class ErrorHandler:
    def __init__(self):
        self.had_error = False

    def error_at_line(self, line, message):
        self.report(line, "", message)

    def error_at_token(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)

    def report(self, line, where, message):
        sys.stderr.write(
            f"[line {line}] Error {where}: {message}"
        )
        sys.stderr.write('\n')
        sys.stderr.flush()
        self.had_error = True


class ParseError(Exception):
    pass


error_handler = ErrorHandler()