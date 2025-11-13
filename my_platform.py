from actor import Actor, Arena, Point

from global_variables import FLOOR_H


class Platform(Actor):
    def __init__(self, pos, size):
        self._x, self._y = pos
        self._w, self._h = size

 
    def move(self, arena: Arena):
        pass

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return None

    def sprite_size(self):
        return None