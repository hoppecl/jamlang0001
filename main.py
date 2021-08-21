#!/usr/bin/env python3

import lark
from lark import ast_utils
import parser
import interpreter
import jltypes
import sys
import jlast

#to_ast_transformer =  #ast_utils.create_transformer(jlast, jlast.ToAst())

def parse_tree_to_ast(parse_tree):
    t = jlast.TransformLiterals().transform(parse_tree)
    return jlast.ToAst().visit(t)

def eval_source(inter, source, print_parse_tree=False):
    try:
        parse_tree = parser.parse(source)
        if print_parse_tree:
            print(parse_tree.pretty())
        ast = parse_tree_to_ast(parse_tree)
        return inter.visit(ast)
    except lark.exceptions.UnexpectedInput as e:
        print(f"{e.line}:{e.column} syntax error"),
        print(e.get_context(source))
    except interpreter.JlTypeError as e:
        print(f"{e.line}:{e.column} type error"),
        print(e.get_context(source))
    except interpreter.UnboundVariable as e:
        print(f"{e.line}:{e.column} unbound variable {e.name.name}"),
        print(e.get_context(source))
        
def run_file(path, print_parse_tree=True, print_value=True, print_env=True):
    with open(path) as f:
        source = f.read()

    i = interpreter.Interpreter()
    value = eval_source(i, source, print_parse_tree)
    if print_value:
        print(value)
    if print_env:
        print(i.environment)

def repl():
    inter = interpreter.Interpreter()
    while True:
        print(">>> ", end='');
        source = input()
        print(eval_source(inter, source, True))

repl()
