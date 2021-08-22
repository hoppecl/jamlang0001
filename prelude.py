from environment import Environment
from jltypes import *


def jl_print(*args):
    if len(args) == 1 and args[0].comment is not None:
        print(str(args[0]),  str(args[0].comment))
    else:
        print(*map(str, args))


def jl_input():
    return JlString(input(), JlComment("the user input"))


prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(jl_print, None, JlComment("the builtin print function")),
    "input": JlPrimitive(jl_input,    0, JlComment("the builtin input function"))
}
