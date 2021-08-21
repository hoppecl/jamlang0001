
class JlException(Exception):
    def __init__(self, source):
        self.line = source.line
        self.column = source.column

    def get_context(self, text):
        line = text.split('\n')[self.line - 1]
        marker = ' ' * (self.column - 1) + '^'
        return line + '\n' + marker
    
class UnboundVariable(JlException):
    def __init__(self, name):
        super().__init__(name.source)
        self.name = name


class JlTypeError(JlException):
    pass

