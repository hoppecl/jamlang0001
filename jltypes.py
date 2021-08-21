from dataclasses import dataclass


class JlComment:
    def __init__(self, text, comment=None):
        self.text = text
        self.comment = comment

    def __repr__(self):
        if self.comment is not None:
            return self.text + str(self.comment)
        return self.text
 
@dataclass
class JlNumber:
    value: float
    comment: JlComment = None

    def __add__(self, other):
        return JlNumber(self.value + other.value, JlComment("/* sum */"))

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


class JlPrimitive:
    def __init__(self, callback, comment=None):
        self.callback = callback
        self.comment = comment

    def __repr__(self):
        return f"JlPrimitive({self.comment})"

    def __call__(self, *args, **kwargs):
        self.callback(*args, **kwargs)


@dataclass
class JlBool:
    value: bool
    comment: JlComment = None

    def __and__(self, other):
        return JlBool(self.value and other.value, JlComment("/* and */"))
