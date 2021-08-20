#!/usr/bin/env python3

import lark
import sys
from dataclasses import dataclass

grammar = r"""

start : stmt+
comment : COMMENT
bool : "true" -> true | "false" -> false

?expr : commented_expr
?commented_expr : or_expr comment
                | or_expr
?or_expr : or_expr "|" and_expr
         | and_expr
?and_expr : and_expr "&" cmp_expr
          | cmp_expr
?cmp_expr : cmp_expr ("==" | "<" | ">")  mul_expr -> bin_op
         | add_expr
!?add_expr : add_expr ("+" | "-") mul_expr -> bin_op
          | mul_expr
!?mul_expr : mul_expr ("*" | "/" | "%") prim_expr -> bin_op
           | prim_expr
?prim_expr : comment
           | group_expr
           | bool
           | SIGNED_NUMBER -> number
           | ESCAPED_STRING -> string
           | "()" -> unit
           | name
           | stmt
?group_expr : "(" expr ")"

?stmt: assign
     | if_stmt
     | while_stmt
     | call_stmt
     | block
assign : name "=" expr
if_stmt : "if" group_expr stmt ["else" stmt]
while_stmt : "while" group_expr stmt
call_stmt : "name" "(" expr ("," expr)* ")"
block : "{" stmt* "}"
name : CNAME

COMMENT : /\/\*[^(\*\/)]*\*\//
%import common.WS
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.CNAME
%ignore WS
"""

parser = lark.Lark(grammar, parser='lalr')

def parse(source):
    return parser.parse(source)

def lex(source):
    return parser.lex(source)
