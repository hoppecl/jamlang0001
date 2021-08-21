import lark
from jltypes import *
import jlast
from copy import copy
from environment import Environment

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


class Resolver(jlast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.scopes = []
        self.scopes.append(set(prelude.bindings.keys()))
        self.scopes.append(set())

    def begin_scope(self):
        self.scopes.append(set())

    def end_scope(self):
        self.scopes.pop(-1)
    
    def visit_block(self, b):
        self.begin_scope()
        for stmt in b.exprs:
            self.visit(stmt)
        self.end_scope()

    def visit_commented_expr(self, e):
        self.visit(e.expr)
        self.visit(e.comment)

    def visit_assignment(self, a):
        self.visit(a.name)
        self.visit(a.expr)
        
    def visit_declaration(self, a):
        self.scopes[-1].add(a.name.name)
        self.visit(a.name)
        self.visit(a.expr)

    def visit_literal(self, l):
        pass

    def visit_name(self, n):
        for i in range(len(self.scopes)):
            if n.name in self.scopes[-i - 1]:
                n.binding_depth = i
                return
        raise UnboundVariable(n)

    def visit_bin_expr(self, e):
        self.visit(e.lhs)
        self.visit(e.rhs)
 
    def visit_and_expr(self, e):
        self.visit(e.lhs)
        self.visit(e.rhs)
        
    def visit_or_expr(self, e):
        self.visit(e.lhs)
        self.visit(e.rhs)

    def visit_call(self, c):
        self.visit(c.f)
        for a in c.args:
            self.visit(a)
        
    def visit_fn_expr(self, f):
        self.begin_scope()
        for p in f.params:
            self.scopes[-1].add(p.name)
        self.visit(f.body)
        self.end_scope()
                
    def visit_explain_expr(self, c):
        self.visit(c.expr)

    def visit_while_expr(self, e):
        self.visit(e.cond)
        self.visit(e.body)

    def visit_if_expr(self, e):
        self.visit(e.cond)
        self.visit(e.then_body)
        if e.else_body is not None:
            self.visit(e.else_body)
    
class Interpreter(jlast.AstVisitor):
    def __init__(self):
        super().__init__()
        self.environment = Environment(prelude)

    def eval_with_env(self, expr, env):
        saved_env = self.environment
        self.environment = env
        value = self.visit(expr)
        self.environment = saved_env
        return value
    
    def visit_block(self, b):
        saved_env = self.environment
        self.environment = Environment(saved_env)
        for stmt in b.exprs:
           value = self.visit(stmt)
        self.environment = saved_env
        return value

    def visit_commented_expr(self, e):
        value = copy(self.visit(e.expr))
        value.comment = self.visit(e.comment)
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
            raise UnboundVariable(n)
        return value

    def visit_bin_expr(self, e):
        lhs = self.visit(e.lhs)
        rhs = self.visit(e.rhs)
        try:
            if e.op == '+':
                return lhs + rhs
            if e.op == '-':
                return lhs - rhs
            if e.op == '*':
                return lhs * rhs
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
        args = list(map(self.visit, c.args))
        if not isinstance(f, JlCallable):
            raise TypeError(c.source)
        r = f.call(self, args)
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
    
prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(print, JlComment("/*the print function*/"))
}
