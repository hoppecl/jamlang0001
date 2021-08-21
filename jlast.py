from dataclasses import dataclass
from lark import ast_utils, visitors, Token
from typing import List
from jltypes import *

@dataclass
class Expr:
    source: object

@dataclass
class CommentedExpr(Expr):
    expr: Expr
    comment: Expr

    def accept(self, visitor):
        return visitor.visit_commented_expr(self)

@dataclass
class BinExpr(Expr):
    lhs: Expr
    op: Token
    rhs: Expr
    
    def accept(self, visitor):
        return visitor.visit_bin_expr(self)
    
    def get_location(self):
        return SourceLoc(self.op.line, self.op.column)

@dataclass
class AndExpr(Expr):
    lhs: Expr
    rhs: Expr
    
    def accept(self, visitor):
        return visitor.visit_and_expr(self)
    
@dataclass
class OrExpr(Expr):
    lhs: Expr
    rhs: Expr
    
    def accept(self, visitor):
        return visitor.visit_or_exp(self)

@dataclass
class Literal(Expr):
    value: object # TODO: JlObject
    def accept(self, visitor):
        return visitor.visit_literal(self)

@dataclass
class Name(Expr):
    name: str
    bind_depth: int = None
    
    def accept(self, visitor):
        return visitor.visit_name(self)


@dataclass
class Assignment(Expr):
    name: Name
    expr: Expr
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)

@dataclass
class IfExpr(Expr):
    cond: Expr
    then_body: Expr
    else_body: Expr = None
    
    def accept(self, visitor):
        return visitor.visit_if_expr(self)

@dataclass
class WhileExpr(Expr):
    cond: Expr
    body: Expr
    
    def accept(self, visitor):
        return visitor.visit_while_expr(self)
    
@dataclass
class CallExpr(Expr):
    f: Expr
    args: List[Expr]
    
    def accept(self, visitor):
        return visitor.visit_call(self)
     
@dataclass
class ExplainExpr(Expr):
    expr: Expr
    
    def accept(self, visitor):
        return visitor.visit_explain_expr(self)
       
@dataclass
class Block(Expr):
    exprs: List[Expr]
    
    def accept(self, visitor):
        return visitor.visit_block(self)

class AstVisitor:
    def visit(self, ast):
        return ast.accept(self)
        
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

    def visit_explain_expr(self, e):
        self.print_indent()
        print("Explain")
        self.indent += 1
        self.visit(e.expr)
        self.indent -= 1
class TransformLiterals(visitors.Transformer):
    def COMMENT(self, c):
        return Literal(c, JlComment(c))

    def SIGNED_NUMBER(self, x):
        return Literal(x, JlNumber(float(x)))

    def ESCAPED_STRING(self, s):
        return Literal(s, JlString(s[1:-1]))
        
    def TRUE(self, t):
        return Literal(t, JlBool(True))
    
    def FALSE(self, f):
        return Literal(f, JlBool(False))

    def UNIT(self, u):
        return Literal(u, JlUnit())

    def CNAME(self, n):
        return str(n)

# would have been nice to use lark.ast_utils for this, but I couldn't figure out how to
# maintain line and column number when using it
class ToAst(visitors.Interpreter):
    def start(self, tree):
        return Block(tree, self.visit_children(tree))

    def block(self, tree):
        return Block(tree, self.visit_children(tree))
        
    def __default__(self, tree):
        print("AAAAAAA", tree)
        return tree
    
    def commented_expr(self, tree):
        return CommentedExpr(tree, *self.visit_children(tree))
    
    def bin_expr(self, tree):
        return BinExpr(tree, *self.visit_children(tree))

    def and_expr(self, tree):
        return AndExpr(tree, *self.visit_children(tree))

    def or_expr(self, tree):
        return AndExpr(tree, *self.visit_children(tree))
    
    def name(self, tree):
        return Name(tree, *self.visit_children(tree))
    
    def assignment(self, tree):
        return Assignment(tree, *self.visit_children(tree))
    
    def if_expr(self, tree):
        return IfExpr(tree, *self.visit_children(tree))
    
    def while_expr(self, tree):
        return WhileExpr(tree, *self.visit_children(tree))
    
    def call_expr(self, tree):
        children = self.visit_children(tree)
        return CallExpr(tree, children[0], children[1:])
    
    def explain_expr(self, tree):
        return ExplainExpr(tree, *self.visit_children(tree))
    
    def block_expr(self, tree):
        return BlockExpr(tree, *self.visit_children(tree))
