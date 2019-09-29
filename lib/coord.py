import operator


class Coord:
    def __init__(self, pos):
        if isinstance(pos, Coord):
            self.pos = (pos.y, pos.x)
            self.y = pos.y
            self.x = pos.x
        else:
            self.pos = pos
            self.y = pos[0]
            self.x = pos[1]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "x":
            self.__dict__["pos"] = (self.pos[0], value)
        elif name == "y":
            self.__dict__["pos"] = (value, self.pos[1])
        elif name == "pos":
            self.__dict__["y"] = self.pos[0]
            self.__dict__["x"] = self.pos[1]

    def __getitem__(self, index):
        if index == 0:
            return self.pos[0]
        elif index == 1:
            return self.pos[1]
        else:
            raise IndexError("list index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.__dict__["pos"] = (value, self.pos[1])
        elif index == 1:
            self.__dict__["pos"] = (self.pos[0], value)
        else:
            raise IndexError("list index out of range")

    def __add__(self, other):
        return self.__class__(tuple(map(operator.add, self.pos, self.__class__(other).pos)))

    def __rep__(self):
        return str(self.pos)

    def __str__(self):
        return str(self.pos)
