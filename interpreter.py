import jlast
from jltypes import *
from copy import copy
from environment import Environment
from prelude import prelude
from exceptions import *
    
class Interpreter(jlast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.environment = Environment(prelude)
        self.backtrace = []

    def eval_with_env(self, expr, env):
        saved_env = self.environment
        self.environment = env
        value = self.visit(expr)
        self.environment = saved_env
        return value

    def clear_backtrace(self):
        self.backtrace = []
        
    def visit_program(self, b):
        for stmt in b.exprs:
           value = self.visit(stmt)
        return value
    
    def visit_block(self, b):
        saved_env = self.environment
        self.environment = Environment(saved_env)
        for stmt in b.exprs:
           value = self.visit(stmt)
        self.environment = saved_env
        return value

    def visit_commented_expr(self, e):
        value = self.visit(e.expr)
        comment = self.visit(e.comment)
        if not isinstance(comment, JlComment):
            raise JlTypeError(self.backtrace, e.source,
                              f"type {type(comment).__name__} can not be used to explain values")
        value = copy(value)
        value.comment = comment
        return value

    def visit_assignment(self, a):
        value = self.visit(a.expr)
        self.environment.put(a.name, value)
        return value
    
    def visit_declaration(self, d):
        value = self.visit(d.expr)
        self.environment.put(d.name, value)
        return value
    
    def visit_declaration(self, a):
        value = self.visit(a.expr)
        self.environment.put(a.name, value)
        return value

    def visit_literal(self, l):
        return l.value

    def visit_name(self, n):
        value = self.environment.get(n)
        if value is None:
            raise UnboundVariable(self.backtrace, n)
        return value

    def visit_bin_expr(self, e):
        lhs = self.visit(e.lhs)
        rhs = self.visit(e.rhs)
        try:
            if e.op == '&':
                return lhs & rhs
            if e.op == '|':
                return lhs | rhs
            if e.op == '+':
                return lhs + rhs
            if e.op == '-':
                return lhs - rhs
            if e.op == '*':
                return lhs * rhs
            if e.op == '*':
                return lhs * rhs
            if e.op == '/':
                return lhs / rhs
            if e.op == '%':
                return lhs % rhs
            if e.op == '==':
                return lhs == rhs
            if e.op == '<':
                return lhs < rhs
            if e.op == '>':
                return lhs > rhs
            assert False
        except TypeError:
            raise JlTypeError(self.backtrace, e.source,
                              f"`{e.op}` not possible for types {type(lhs).__name__} and {type(rhs).__name__}")

    def visit_and_expr(self, e):
        return self.visit(e.lhs) & self.visit(e.rhs)
        
    def visit_or_expr(self, e):
        lhs = self.visit(e.lhs)
        if not lhs.value:
            return self.visit(e.rhs)
        return lhs

    def visit_call(self, c):
        f = self.visit(c.f)
        args = list(map(self.visit, c.args))
        if not isinstance(f, JlCallable):
            raise JlTypeError(self.backtrace,
                              c.source, f"{type(f).__name__} is not callable")
        self.backtrace.append(c.source)
        r = f.call(self, args)
        self.backtrace.pop()
        if r is None:
            return JlUnit()
        else:
            return r
        
    def visit_fn_expr(self, f):
        return JlClosure(self.environment, f.params, f.body)
        
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
    
