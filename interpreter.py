import lark
from jltypes import *
import jlast
from copy import copy

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
    
class Environment:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def put(self, name, value):
        self.bindings[name] = value

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name)
        return None

class Interpreter(jlast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.environment = Environment(prelude)
        
    def visit_block(self, b):
        for stmt in b.exprs:
           value = self.visit(stmt)
        return value

    def visit_commented_expr(self, e):
        value = copy(self.visit(e.expr))
        value.comment = self.visit(e.comment)
        return value

    def visit_assignment(self, a):
        value = self.visit(a.expr)
        print("ASS", a.name.name, value)
        self.environment.put(a.name.name, value)
        return value

    def visit_literal(self, l):
        return l.value

    def visit_name(self, n):
        value = self.environment.get(n.name)
        if value is None:
            raise UnboundVariable(n)
        return value

    def visit_bin_expr(self, e):
        lhs = self.visit(e.lhs)
        rhs = self.visit(e.rhs)
        try:
            if e.op == '+':
                return lhs + rhs
            if e.op == '%':
                return lhs % rhs
            if e.op == '==':
                return lhs == rhs
            if e.op == '<':
                return lhs < rhs
        except TypeError:
            raise JlTypeError(e.source)

    def visit_and_expr(self, e):
        lhs = self.visit(e.lhs)
        if lhs.value:
            return self.visit(e.rhs)
        return lhs
        
    def visit_or_expr(self, e):
        lhs = self.visit(e.lhs)
        if not lhs.value:
            return self.visit(e.rhs)
        return lhs

    def visit_call(self, c):
        f = self.visit(c.f)
        args = map(self.visit, c.args)
        r = f(*args)
        if r is None:
            return JlUnit()
        else:
            return r
        
    def visit_explain_expr(self, c):
        value = self.visit(c.expr)
        if value.comment is None:
            return JlUnit()
        return value.comment

    def visit_while_expr(self, e):
        while self.visit(e.cond).value:
            value = self.visit(e.body)
        return value

    def visit_if_expr(self, e):
        if self.visit(e.cond).value:
            return self.visit(e.then_body)
        elif e.else_body is not None:
            return self.visit(e.else_body)
        return JlUnit()
    
prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(print, JlComment("/*the print function*/"))
}
