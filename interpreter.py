import lark
from jltypes import *
from copy import copy

class UnboundVariable(Exception):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Unbound Variable: {self.name}"

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
        raise UnboundVariable(name)

class Interpreter(lark.visitors.Interpreter):
    def __init__(self):
        super().__init__()
        self.environment = Environment()
        
    def start(self, tree):
        for stmt in tree.children:
            print(self.visit(stmt))
        return None

    def commented_expr(self, token):
        comment = self.visit(token.children[1])
        value = copy(self.visit(token.children[0]))
        value.comment = comment
        return value
    
    def comment(self, tree):
        return JlComment(tree.children[0])

    def assign(self, tree):
        name = str(tree.children[0].children[0])
        value = self.visit(tree.children[1])
        print(name)
        self.environment.put(name, value)
        return value

    def number(self, tree):
        value = float(tree.children[0])
        return JlNumber(value)

    def string(self, tree):
        value = str(tree.children[0])[1:-1]
        return JlString(value)

    def unit(self, tree):
        return JlUnit()

    def name(self, tree):
        name = str(tree.children[0])
        value = self.environment.get(name)
        return value

    def bin_op(self, tree):
        lhs = self.visit(tree.children[0])
        rhs = self.visit(tree.children[2])
        op = tree.children[1]
        if op == '+':
            return lhs + rhs
        
