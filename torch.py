from actor import Actor, Arena, Point
from flame import Flame
from actor import check_collision
from global_variables import GRAVITY, FLOOR_H

class Torch(Actor):
    def __init__(self, pos, direction):
        self._x, self._y = pos
        self._w, self._h = 12, 12
        
        self._falling_speed = 0
        self._speed_x = 3 if direction == "right" else -3
        self._direction = direction

        self._frames = [
            (210, 443),
            (230, 443),
            (250, 443),
            (270, 443),
        ]
        self._frame_size = (16, 16)

        self._frame_counter = 0
        self._animation_speed = 5  # cambia frame ogni 5 tick

    # ---------------------------------------------------------

    def move(self, arena: Arena):

        # Animazione
        self._frame_counter += 1
        self._frame_counter %= len(self._frames) * self._animation_speed

        # Movimento orizzontale
        self._x += self._speed_x

        # Gravità
        self._falling_speed += GRAVITY
        self._y += self._falling_speed

        # Rimbalzo sul terreno → fiamma
        if self._y >= FLOOR_H:
            self._y = FLOOR_H
            arena.spawn(Flame((self._x, self._y)))
            arena.kill(self)
            return

        # Collisioni
        for other in arena.actors():
            if other is self:
                continue

            if other.__class__.__name__ == "Zombie":
                other.hit(arena)
                arena.kill(self)
                return

            if type(other).__name__ in ("Gravestone", "Platform") and check_collision(self, other):
                arena.spawn(Flame((self._x, self._y)))
                arena.kill(self)
                return

        # Limiti arena
        aw, ah = arena.size()
        if self._x < 0 or self._x > aw:
            arena.kill(self)

    # ---------------------------------------------------------

    def sprite(self) -> Point:
        index = self._frame_counter // self._animation_speed
        return self._frames[index]

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        index = self._frame_counter // self._animation_speed
        return self._frames[index]

    def sprite_size(self) -> Point:
        return self._frame_size