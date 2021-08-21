from environment import Environment
from jltypes import *


prelude = Environment()
prelude.bindings = {
    "print": JlPrimitive(print, JlComment("/*the print function*/"))
}
