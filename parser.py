#!/usr/bin/env python3

import lark
import sys
from dataclasses import dataclass

grammar = r"""

start : stmt+
TRUE: "true"
FALSE: "false"
?expr : commented_expr
?commented_expr : or_expr commented_expr
                | or_expr
?or_expr : or_expr "|" and_expr
         | and_expr
?and_expr : and_expr "&" cmp_expr
          | cmp_expr
!?cmp_expr : cmp_expr ("==" | "<" | ">")  mul_expr -> bin_expr
         | add_expr
!?add_expr : add_expr ("+" | "-") mul_expr -> bin_expr
          | mul_expr
!?mul_expr : mul_expr ("*" | "/" | "%") prim_expr -> bin_expr
           | prim_expr
?prim_expr : COMMENT
           | group_expr
           | TRUE
           | FALSE
           | SIGNED_NUMBER
           | ESCAPED_STRING
           | UNIT
           | name
           | assignment
           | declaration
           | if_expr
           | while_expr
           | call_expr
           | fn_expr
           | explain_expr
           | block
?group_expr : "(" expr ")"
?stmt: expr ";"

assignment : name "=" expr
declaration : "let" name "=" expr
if_expr : "if" group_expr expr ["else" expr]
while_expr : "while" group_expr expr
call_expr : prim_expr "(" [expr ("," expr)*] ")"
fn_expr : "fn" "(" [name ("," name)*] ")" expr
explain_expr : prim_expr "?"
block : "{" stmt* "}"
name : CNAME

UNIT: "()"
COMMENT : /\/\*[^(\*\/)]*\*\//
%import common.WS
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.CNAME
%ignore WS
"""

parser = lark.Lark(grammar, parser='lalr', propagate_positions=True)
expr_parser = lark.Lark(grammar, start='expr', parser='lalr', propagate_positions=True)
def parse(source):
    return parser.parse(source)
