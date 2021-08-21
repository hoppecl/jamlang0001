#!/usr/bin/env python3

import lark
import sys
from parser import parser
from jlast import TransformLiterals, ToAst, AstPrinter
from interpreter import Interpreter
from resolver import Resolver
from exceptions import JlTypeError, UnboundVariable

to_ast_transformer =  ToAst()
literal_transformer = TransformLiterals()


def eval_source(interpreter, source, debug=True):
    try:
        parse_tree = parser.parse(source)
        if debug:
            print(parse_tree.pretty())
    
        tree_with_literals = literal_transformer.transform(parse_tree)
        ast = to_ast_transformer.visit(tree_with_literals)
        Resolver(interpreter.environment).visit(ast)
        if debug:
            AstPrinter().visit(ast)

        return interpreter.visit(ast)

    except lark.exceptions.UnexpectedInput as e:
        print(f"{e.line}:{e.column} syntax error"),
        print(e.get_context(source))
    except JlTypeError as e:
        print(f"{e.line}:{e.column} type error: {e.msg}"),
        print(e.get_context(source))
    except UnboundVariable as e:
        print(f"{e.line}:{e.column} unbound variable {e.name.name}"),
        print(e.get_context(source))


def run_file(path, debug=False):
    with open(path) as f:
        source = f.read()

    i = Interpreter()
    value = eval_source(i, source, debug=debug)
    if debug:
        print(value)
    if debug:
        print(i.environment.bindings)

def repl():
    inter = Interpreter()
    while True:
        print(">>> ", end='');
        source = input()
        print(eval_source(inter, source, True))
        print(inter.environment.bindings)

if len(sys.argv) >= 2:
    run_file(sys.argv[1])
else:
    repl()
