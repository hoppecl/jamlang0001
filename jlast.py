from dataclasses import dataclass
from lark import ast_utils, visitors
from typing import List
from jltypes import *

class _Expr(ast_utils.Ast):
    pass

@dataclass
class CommentedExpr(_Expr):
    expr: _Expr
    comment: _Expr

    def accept(self, visitor):
        visitor.visit_commented_expr(self)

@dataclass
class BinExpr(_Expr):
    lhs: _Expr
    op: str
    rhs: _Expr
    
    def accept(self, visitor):
        visitor.visit_bin_expr(self)

@dataclass
class AndExpr(_Expr):
    lhs: _Expr
    rhs: _Expr
    
    def accept(self, visitor):
        visitor.visit_and_expr(self)
    
@dataclass
class OrExpr(_Expr):
    lhs: _Expr
    rhs: _Expr
    
    def accept(self, visitor):
        visitor.visit_or_exp(self)

@dataclass
class Literal(_Expr):
    value: object # TODO: JlObject
    def accept(self, visitor):
        visitor.visit_literal(self)

@dataclass
class Name(_Expr):
    name: str
    bind_depth: int = None
    
    def accept(self, visitor):
        visitor.visit_name(self)

@dataclass
class Assignment(_Expr):
    name: Name
    expr: _Expr
    
    def accept(self, visitor):
        visitor.visit_assignment(self)

@dataclass
class IfExpr(_Expr):
    cond: _Expr
    then_body: _Expr
    else_body: _Expr = None
    
    def accept(self, visitor):
        visitor.visit_if_expr(self)

@dataclass
class WhileExpr(_Expr):
    cond: _Expr
    body: _Expr
    
    def accept(self, visitor):
        visitor.visit_while_expr(self)
    
@dataclass
class CallExpr(_Expr):
    def __init__(self, f, *args):
        self.f = f
        self.args = args
    f: _Expr
    args: List[_Expr]
    
    def accept(self, visitor):
        visitor.visit_call(self)
    
@dataclass
class Block(_Expr, ast_utils.AsList):
    exprs: List[_Expr]
    
    def accept(self, visitor):
        visitor.visit_block(self)

class AstVisitor:
    def visit(self, ast):
        ast.accept(self)
        
class AstPrinter(AstVisitor):
    def __init__(self):
        self.indent = 0

    def print_indent(self):
        print(" |" * self.indent, end='')

    def visit_block(self, block):
        self.print_indent()
        print('Block')
        self.indent += 1
        for e in block.exprs:
            self.visit(e)
        self.indent -= 1

    def visit_literal(self, lit):
        self.print_indent()
        print(lit.value)

    def visit_assignment(self, a):
        self.print_indent()
        print("Assignment", end='')
        self.visit(a.name)
        self.indent += 1
        self.visit(a.expr)
        self.indent -= 1

    def visit_name(self, a):
        self.print_indent()
        print(f"<{a.name}>")

    def visit_commented_expr(self, e):
        self.print_indent()
        print("Commented Expr")
        self.indent += 1
        self.visit(e.expr)
        self.visit(e.comment)
        self.indent -= 1

    def visit_while_expr(self, e):
        self.print_indent()
        print("While")
        self.indent += 1
        self.visit(e.cond)
        self.visit(e.body)
        self.indent -= 1

    def visit_bin_expr(self, e):
        self.print_indent()
        print("BinExpr", e.op)
        self.indent += 1
        self.visit(e.lhs)
        self.visit(e.rhs)
        self.indent -= 1
        
    def visit_and_expr(self, e):
        self.print_indent()
        print("And")
        self.indent += 1
        self.visit(e.lhs)
        self.visit(e.rhs)
        self.indent -= 1
        
    def visit_or_expr(self, e):
        self.print_indent()
        print("Or")
        self.indent += 1
        self.visit(e.lhs)
        self.visit(e.rhs)
        self.indent -= 1
        
    def visit_if_expr(self, e):
        self.print_indent()
        print("If")
        self.indent += 1
        self.visit(e.cond)
        self.visit(e.then_body)
        if e.else_body is not None:
            self.visit(e.else_body)
        self.indent -= 1

    def visit_call(self, e):
        self.print_indent()
        print("Call")
        self.indent += 1
        self.visit(e.f)
        for a in e.args:
            self.visit(a)
        self.indent -= 1
        
        
        
    
class ToAst(visitors.Transformer):
    def start(self, exprs):
        return Block(exprs)
    
    def COMMENT(self, c):
        return Literal(JlComment(c))

    def SIGNED_NUMBER(self, x):
        return Literal(JlNumber(float(x)))

    def ESCAPED_STRING(self, s):
        return Literal(JlString(s[1:-1]))
        
    def TRUE(self):
        return Literal(JlBool(True))
    
    def FALSE(self):
        return Literal(JlBool(False))

    def UNIT(self):
        return Literal(JlBool(False))

    def CNAME(self, n):
        return str(n)

