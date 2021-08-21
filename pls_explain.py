#!/usr/bin/env python3

import lark
import sys
from parser import parser
from jlast import TransformLiterals, ToAst, AstPrinter
from interpreter import Interpreter
from resolver import Resolver
from exceptions import JlException

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

    except lark.exceptions.UnexpectedToken as e:
        print(f"{e.line}:{e.column} syntax error: expected one of {e.expected}"),
        print(e.get_context(source))
    except lark.exceptions.UnexpectedCharacters as e:
        print(f"{e.line}:{e.column} syntax error: unexpected characters"),
        print(e.get_context(source))
    except lark.exceptions.UnexpectedEOF as e:
        print(f"{e.line}:{e.column} syntax error: unexpected end of file"),
        print(e.get_context(source))
    except JlException as e:
        print(e.get_backtrace(source))


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
        try:
            source = input()
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break
        print(eval_source(inter, source, True))
        inter.clear_backtrace()

if len(sys.argv) >= 2:
    run_file(sys.argv[1])
else:
    repl()
