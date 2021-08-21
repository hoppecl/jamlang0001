from dataclasses import dataclass
from environment import Environment


class JlComment:
    def __init__(self, text, comment=None):
        self.text = text
        self.comment = comment

    def __repr__(self):
        if self.comment is not None:
            return '/*' + self.text + " " + '*/' + str(self.comment)
        return '/*' + self.text + '*/'
    
    def __add__(self, other):
        if not isinstance(other, JlComment):
            raise TypeError()
        return JlComment(self.text + other.text)

class JlValue:
    def __str__(self):
        if self.comment is not None:
            return str(self.value) + " " + str(self.comment)
        return str(self.value)

@dataclass
class JlNumber(JlValue):
    value: float
    comment: JlComment = None
    
    def __init__(self, value, comment=None):
        self.value = value
        if comment is None:
            comment = JlComment(f"the number {value}")
        self.comment = comment

    def build_comment(self, name, other):
        return JlComment(f"the {name} of {self.comment.text} and {other.comment.text}")

    def __add__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlNumber(self.value + other.value,
                        self.build_comment("sum", other))

    def __sub__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlNumber(self.value - other.value,
                        self.build_comment("difference", other))

    def __mul__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlNumber(self.value * other.value,
                        self.build_comment("product", other))
    
    def __truediv__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlNumber(self.value / other.value,
                        self.build_comment("quotient", other))

    def __mod__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlNumber(self.value % other.value,
                        self.build_comment("modulus", other))

    def __eq__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlBool(self.value == other.value,
                      JlComment(f"{self.comment.text} is equal to {other.comment.text}"))

    def __lt__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlBool(self.value < other.value, 
                      JlComment(f"{self.comment.text} is less than {other.comment.text}"))

    def __gt__(self, other):
        if not isinstance(other, JlNumber):
            raise TypeError()
        return JlBool(self.value > other.value, 
                      JlComment(f"{self.comment.text} is greater than {other.comment.text}"))


@dataclass
class JlString(JlValue):
    value: str
    comment: JlComment = None

    def __init__(self, value, comment=None):
        self.value = value
        if comment is None:
            comment = JlComment(f"the string \"{value}\"")
        self.comment = comment


@dataclass
class JlUnit:
    comment: JlComment = JlComment("unit")

    def __str__(self):
        if self.comment is not None:
            return "() " + str(self.comment)
        return "()"


@dataclass
class JlBool(JlValue):
    value: bool
    comment: JlComment = None

    def __init__(self, value, comment=None):
        self.value = value
        if comment is None:
            comment = JlComment(f"the boolean \"{value}\"")
        self.comment = comment

    def __and__(self, other):
        if not isinstance(other, JlBool):
            raise TypeError()
        return JlBool(self.value and other.value,
                      JlComment(f"{self.comment.text} and {other.comment.text}"))

    def __or__(self, other):
        if not isinstance(other, JlBool):
            raise TypeError()
        return JlBool(self.value and other.value,
                      JlComment(f"{self.comment.text} or {other.comment.text}"))
    
    def __eq__(self, other):
        if not isinstance(other, JlBool):
            raise TypeError()
        return JlBool(self.value and other.value,
                      JlComment(f"{self.comment.text} is equal to {other.comment.text}"))

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

