#!/usr/bin/env python3

import lark
import sys
import argparse
from parser import parser
from jlast import TransformLiterals, ToAst, AstPrinter
from interpreter import Interpreter
from resolver import Resolver
from exceptions import JlException
from jltypes import JlUnit, JlComment


to_ast_transformer = ToAst()
literal_transformer = TransformLiterals()


def eval_source(interpreter, source, debug=True):
    try:
        parse_tree = parser.parse(source)
        if debug:
            print("Parse Tree:")
            print(parse_tree.pretty())
            print()
    
        tree_with_literals = literal_transformer.transform(parse_tree)
        ast = to_ast_transformer.visit(tree_with_literals)
        Resolver(interpreter.environment).visit(ast)
        if debug:
            print("Abstract Syntax Tree:")
            AstPrinter().visit(ast)
            print()

        value = interpreter.visit(ast)

        if debug:
            print("Global Environment after Evaluation:")
            for k, v in interpreter.environment.bindings.items():
                print(f"{k} = {repr(v)} {v.comment or ''}")
            print()

        return value

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

    return JlUnit(JlComment(":("))


def run_file(path, debug=False):
    with open(path) as f:
        source = f.read()

    i = Interpreter()
    value = eval_source(i, source, debug=debug)
    if debug:
        print("Program Return Value:")
        print(value)


def repl(debug=True):
    inter = Interpreter()
    while True:
        print(">>> ", end='')
        try:
            source = input()
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break
        value = eval_source(inter, source, debug)
        print("->", value, value.comment or "")
        inter.clear_backtrace()


if __name__ == "__main__":
    argp = argparse.ArgumentParser(
        description="A programming language  with first-class Comments")
    argp.add_argument("file", type=str, nargs='?',
                      help="PlsExplain program to run")
    argp.add_argument("-d", "--debug", default=False, action="store_true",
                      help="print verbose debug info")
    args = argp.parse_args()
    if args.file is not None:
        run_file(args.file, args.debug)
    else:
        repl(args.debug)
