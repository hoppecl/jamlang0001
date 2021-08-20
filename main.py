#!/usr/bin/env python3

import lark
import parser
import interpreter
import jltypes
import sys

with open(sys.argv[1]) as f:
    source = f.read()

try:
    ast = parser.parse(source)
    print(ast.pretty())
    i = interpreter.Interpreter()
    print(i.visit(ast))
    print(i.environment.bindings)
except lark.exceptions.UnexpectedInput as e:
    print(e)
    print(e.get_context(source))
