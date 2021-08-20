#!/usr/bin/env python3

import lark
import sys
from dataclasses import dataclass

grammar = r"""

comment : COMMENT [comment]
start : [comment] stmt+ 
number : SIGNED_NUMBER [comment]
string : ESCAPED_STRING [comment]
true : "True" [comment]
false: "False" [comment]
bool : true | false

?expr : or_expr
?or_expr : or_expr or and_expr -> or
         | and_expr
?and_expr : and_expr and cmp_expr -> and
          | cmp_expr
?cmp_expr : cmp_expr equalequal mul_expr -> equal
         | cmp_expr less mul_expr  -> less
         | cmp_expr greater mul_expr  -> greater
         | add_expr
?add_expr : add_expr plus mul_expr
          | add_expr minus mul_expr
          | mul_expr
?mul_expr : mul_expr star prim_expr
          | mul_expr slash prim_expr
          | mul_expr percent prim_expr
          | prim_expr
?prim_expr : group_expr
           | bool
           | number
           | string
           | unit
           | name
           | stmt
group_expr : lparen expr rparen

?stmt: assign
     | if_stmt
     | while_stmt
     | call_stmt
     | block
assign : name equal expr
if_stmt : if group_expr stmt [else stmt]
while_stmt : while group_expr stmt
call_stmt : name lparen expr (comma expr)* rparen
block : lbrace stmt* rbrace

_token{t}: t [comment]
or         : _token{"|"}
and        : _token{"&"}
equalequal : _token{"=="}
equal       : _token{"="}
less       : _token{"<"}
greater    : _token{">"}
plus       : _token{"+"}
minus      : _token{"-"}
star       : _token{"*"}
slash      : _token{"/"}
name       : _token{CNAME}
lparen     : _token{"("}
rparen     : _token{")"}
lbrace     : _token{"{"}
rbrace     : _token{"}"}
if         : _token{"if"}
else       : _token{"else"}
while      : _token{"while"}
semicolon  : _token(";")
comma      : _token{","}
percent    : _token{"%"}
unit       : _token{"()"}

COMMENT : /\/\*[^(\*\/)]*\*\//
%import common.WS
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.CNAME
%ignore WS
"""

parser = lark.Lark(grammar)

def parse(source):
    return parser.parse(source)
