#!/usr/bin/env python3

import lark
import sys
from dataclasses import dataclass

grammar = r"""

start : stmt+
bool : "true" -> true | "false" -> false

?expr : commented_expr
?commented_expr : or_expr commented_expr
                | or_expr
?or_expr : or_expr "|" and_expr
         | and_expr
?and_expr : and_expr "&" cmp_expr
          | cmp_expr
!?cmp_expr : cmp_expr ("==" | "<" | ">")  mul_expr -> bin_op
         | add_expr
!?add_expr : add_expr ("+" | "-") mul_expr -> bin_op
          | mul_expr
!?mul_expr : mul_expr ("*" | "/" | "%") prim_expr -> bin_op
           | prim_expr
?prim_expr : COMMENT -> comment
           | group_expr
           | bool
           | SIGNED_NUMBER -> number
           | ESCAPED_STRING -> string
           | "()" -> unit
           | name
           | assign
           | if_expr
           | while_expr
           | call_expr
           | block
?group_expr : "(" expr ")"
?stmt: expr ";"

assign : name "=" expr
if_expr : "if" group_expr expr ["else" expr]
while_expr : "while" group_expr expr
call_expr : prim_expr "(" [expr ("," expr)*] ")"
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
