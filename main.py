#!/usr/bin/env python3

import lark
from lark import ast_utils
import parser
import interpreter
import jltypes
import sys
import jlast

to_ast_transformer = ast_utils.create_transformer(jlast, jlast.ToAst())

def parse_tree_to_ast(parse_tree):
    return to_ast_transformer.transform(parse_tree)

with open(sys.argv[1]) as f:
    source = f.read()

try:
    parse_tree = parser.parse(source)
    print(parse_tree.pretty())
    ast = parse_tree_to_ast(parse_tree)
    jlast.AstPrinter().visit(ast)
    #i = interpreter.Interpreter()
    #print(i.visit(ast))
    #print(i.environment.bindings)
except lark.exceptions.UnexpectedInput as e:
    print(e)
    print(e.get_context(source))
