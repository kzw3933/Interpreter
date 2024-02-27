import sys

class ErrorHandler:
    def __init__(self):
        self.had_error = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        sys.stderr.write(
            f"[line {line}] Error{where}: {message}"
        )
        sys.stderr.write('\n')
        sys.stderr.flush()
        self.had_error = True

error_handler = ErrorHandler()