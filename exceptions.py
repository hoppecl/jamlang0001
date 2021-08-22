class JlException(Exception):
    def __init__(self, backtrace, source):
        self.backtrace = backtrace + [source]

    def get_context(self, location, text):
        lines = text.split('\n')
        if location.line == location.end_line:
            line = lines[location.line - 1]
            marker = ' ' * (location.column - 1) + '^' + \
                '~' * (location.end_column - location.column - 1)
            return line + '\n' + marker
        else:
            first_line = lines[location.line - 1]
            last_line = lines[location.end_line - 1]
            marker = ' ' * (location.column - 1) + '^' + \
                '~' * (len(first_line) - location.column)
            end_marker = '~' * (location.end_column - 1)
            msg = first_line + '\n' + marker + '\n'
            if location.end_line != location.line + 1:
                msg += '...\n'
            msg += last_line + '\n' + end_marker
            return msg

    def get_backtrace(self, text):
        bt = "Backtrace (most recent call last):\n\n"
        for loc in self.backtrace:
            bt += f"line {loc.line}:\n"
            bt += self.get_context(loc, text) + '\n'
        return bt + '\n' + str(self)


class UnboundVariable(JlException):
    def __init__(self, name):
        super().__init__([], name.source)
        self.name = name

    def __str__(self):
        return f"unbound variable {self.name.name}"


class JlTypeError(JlException):
    def __init__(self, bt, expr, msg):
        super().__init__(bt, expr)
        self.msg = msg

    def __str__(self):
        return f"type error: {self.msg}"

