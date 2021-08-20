import lark
from jltypes import *
from copy import copy

class UnboundVariable(Exception):
    pass

class Environment:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def put(self, name, value, comment=None):
        self.bindings[name] = value

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if parent is not None:
            return self.parent.get(name)
        raise UnboundVariable()

class Interpreter(lark.visitors.Interpreter):
    def __init__(self):
        super().__init__()
        self.environment = Environment()
        
    def start(self, tree):
        for stmt in tree.children:
            print(self.visit(stmt))
        return None

    def token_comment(self, token, index=1):
        if len(token.children) >= index + 1:
            return self.visit(token.children[index])
        return None
    
    def comment(self, tree):
        meta_comment = self.token_comment(tree)
        return JlComment(tree.children[0], meta_comment)

    def assign(self, tree):
        name = tree.children[0]
        name_comment = self.token_comment(name)
        comment = self.token_comment(tree.children[1])
        value = self.visit(tree.children[2])
            
        self.environment.put(str(name.children[0]), value, name_comment)
        return value

    def number(self, tree):
        comment = self.token_comment(tree)
        value = float(tree.children[0])
        return JlNumber(value, comment)

    def string(self, tree):
        comment = self.token_comment(tree)
        value = str(tree.children[0])[1:-1]
        return JlString(value, comment)

    def unit(self, tree):
        comment = self.token_comment(tree, 0)
        return JlUnit(comment)

    def name(self, tree):
        comment = self.token_comment(tree)
        name = str(tree.children[0])
        value = self.environment.get(name)
        if comment is not None:
            value = copy(value)
            value.comment = comment
        return value
