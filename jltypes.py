from dataclasses import dataclass
from environment import Environment

class JlComment:
    def __init__(self, text, comment=None):
        self.text = text
        self.comment = comment

    def __repr__(self):
        if self.comment is not None:
            return '/*' + self.text + '*/' + str(self.comment)
        return self.text
    
    def __add__(self, other):
        return JlComment(self.text + other.text, JlComment("/* sum */"))
 
@dataclass
class JlNumber:
    value: float
    comment: JlComment = None

    def __add__(self, other):
        return JlNumber(self.value + other.value, JlComment("/* sum */"))
    
    def __sub__(self, other):
        return JlNumber(self.value - other.value, JlComment("/* difference */"))
    
    def __mul__(self, other):
        return JlNumber(self.value * other.value, JlComment("/* product */"))

    def __mod__(self, other):
        return JlNumber(self.value % other.value, JlComment("/* modulo */"))
        
    def __eq__(self, other):
        return JlBool(self.value == other.value, JlComment("/* equal */"))
    
    def __lt__(self, other):
        return JlBool(self.value < other.value, JlComment("/* less */"))


@dataclass
class JlString:
    value: str
    comment: JlComment = None


@dataclass
class JlUnit:
    comment: JlComment = None

@dataclass
class JlBool:
    value: bool
    comment: JlComment = None

    def __and__(self, other):
        return JlBool(self.value and other.value, JlComment("/* and */"))

class JlCallable:
    pass

class JlPrimitive(JlCallable):
    def __init__(self, callback, comment=None):
        self.callback = callback
        self.comment = comment

    def __repr__(self):
        return f"JlPrimitive({self.comment})"

    def call(self, interpreter, args):
        self.callback(*args)


class JlClosure(JlCallable):
    def __init__(self, environment, params, body, comment=None):
        self.environment = environment
        self.params = params
        self.body = body
        self.comment = comment

    def __repr__(self):
        return f"JlClosure()"

    def call(self, interpreter, args):
        env = Environment(self.environment)
        for p, a in zip(self.params, args):
            env.put(p, a, 0)
        return interpreter.eval_with_env(self.body, env)

