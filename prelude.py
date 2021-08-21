from environment import Environment
from jltypes import *


def jl_print(*args):
    print(*map(str, args))


prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(jl_print, JlComment("/*the print function*/"))
}
