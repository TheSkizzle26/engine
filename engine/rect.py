import engine


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    #----------DEFAULT----------

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = int(val)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = int(val)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = int(val)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = int(val)

    #----------SINGLE----------

    @property
    def top(self):
        return self._y

    @top.setter
    def top(self, val):
        self.y = val

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, val):
        self.y = val - self.height

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, val):
        self.x = val

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, val):
        self.x = val - self.width

    # ----------DOUBLE----------

    @property
    def topleft(self):
        return self.x, self.y

    @topleft.setter
    def topleft(self, val):
        self.x = val[0]
        self.y = val[1]

    @property
    def topright(self):
        return self.x + self.width, self.y

    @topright.setter
    def topright(self, val):
        self.x = val[0] - self.width
        self.y = val[1]

    @property
    def bottomleft(self):
        return self.x, self.y + self.height

    @bottomleft.setter
    def bottomleft(self, val):
        self.x = val[0]
        self.y = val[1] - self.height

    @property
    def bottomright(self):
        return self.x + self.width, self.y + self.height

    @bottomright.setter
    def bottomright(self, val):
        self.x = val[0] - self.width
        self.y = val[1] - self.height

    @property
    def center(self):
        return self.x + self.width/2, self.y + self.height/2

    @center.setter
    def center(self, val):
        self.x = val[0] - self.width/2
        self.y = val[1] - self.height/2

    def collidepoint(self, val):
        return (self.x <= val[0] < self.x + self.width) and (self.y <= val[1] < self.y + self.height)

    def colliderect(self, rect: "Rect"):
        return (self.x < rect.x + rect.width) and \
               (self.x + self.width > rect.x) and \
               (self.y < rect.y + rect.height) and \
               (self.y + self.height > rect.y)

class FRect(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #----------OVERRIDES----------

    # just the above but without converting everything to an int

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val