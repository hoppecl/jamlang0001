#!/usr/bin/env python3

import lark
import sys
import parser
from jlast import TransformLiterals, ToAst, AstPrinter
from interpreter import Interpreter
from resolver import Resolver

to_ast_transformer =  ToAst()
literal_transformer = TransformLiterals()
resolver = Resolver()


def eval_source(interpreter, source, print_parse_tree=False, print_ast=True):
    try:
        parse_tree = parser.parse(source)
        if print_parse_tree:
            print(parse_tree.pretty())
            
        tree_with_literals = literal_transformer.transform(parse_tree)
        ast = to_ast_transformer.visit(tree_with_literals)
        resolver.visit(ast)
        if print_ast:
            AstPrinter().visit(ast)
            
        return interpreter.visit(ast)
    
    except lark.exceptions.UnexpectedInput as e:
        print(f"{e.line}:{e.column} syntax error"),
        print(e.get_context(source))
    except interpreter.JlTypeError as e:
        print(f"{e.line}:{e.column} type error"),
        print(e.get_context(source))
    except interpreter.UnboundVariable as e:
        print(f"{e.line}:{e.column} unbound variable {e.name.name}"),
        print(e.get_context(source))
        
def run_file(path, print_value=True, debug=True):
    with open(path) as f:
        source = f.read()

    i = Interpreter()
    value = eval_source(i, source, debug, debug)
    if print_value:
        print(value)
    if debug:
        print(i.environment.bindings)

def repl():
    inter = Interpreter()
    while True:
        print(">>> ", end='');
        source = input()
        print(eval_source(inter, source, True))

if len(sys.argv) >= 2:
    run_file(sys.argv[1])
else:
    repl()
