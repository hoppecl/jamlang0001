from environment import Environment
from jltypes import *


def jl_print(*args):
    if len(args) == 1:
        print(str(args[0]),  str(args[0].get_comment()))
    else:
        print(*map(str, args))


def jl_input():
    return JlString(input(), JlComment("the user input"))


def jl_str(arg):
    return JlString(str(arg), JlComment(f"{arg.get_comment().value} as a string"))


def jl_cmnt(arg):
    return JlComment(str(arg), JlComment(f"{arg.get_comment().value} as a comment"))


prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(jl_print, None, JlComment("the builtin print function")),
    "input": JlPrimitive(jl_input, 0, JlComment("the builtin input function")),
    "str": JlPrimitive(jl_str, 1, JlComment("the builtin str function")),
    "cmnt": JlPrimitive(jl_cmnt, 1, JlComment("the builtin cmnt function")),
}
