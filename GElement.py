from enum import Enum


class GType(Enum):
    NonTerm_simpl = 0
    NonTerm_box = 1
    Terminal = 2


class Gelemnt:
    def __init__(self, gtype: GType, data):
        self.type = gtype
        self.data = data

    def __str__(self):
        if self.type == GType.NonTerm_box:
            return f"[{self.data[0]},{self.data[1]}]"
        else:
            return f"<{self.data}>"

    def __eq__(self, other):
        if not(type(other) is Gelemnt):
            return False
        if self.type != other.type:
            return False
        if self.type == GType.NonTerm_box:
            if not(self.data[0] == other.data[0] and self.data[1] == other.data[1]):
                return False
        else:
            if not(self.data == other.data):
                return False

        return True

    def __hash__(self):
        if self.type == GType.NonTerm_box:
            return hash((self.type, self.data[0], self.data[1]))
        else:
            return hash((self.type, self.data))
