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
        return JlNumber(self.value + other.value, "/* sum */")


@dataclass
class JlString:
    value: str
    comment: JlComment = None


@dataclass
class JlUnit:
    comment: JlComment = None
