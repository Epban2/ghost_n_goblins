from actor import Actor, Arena, Point, check_collision
from flame import Flame
from global_variables import TORCH_GRAVITY, GROUND_H

class Torch(Actor):
    def __init__(self, pos, direction):
        self._x, self._y = pos
        self._w, self._h = 15, 15
        
        self._falling_speed = 0
        self._speed_x = 3 if direction == "right" else -3
        self._direction = direction

        self._frames = [
            (19, 399),
            (39, 399),
            (59, 399),
            (79, 399)
        ]

        self._frame_size = (15, 15)

        self._frame_counter = 0
        self._animation_speed = 5  # cambia frame ogni 5 tick

    # ---------------------------------------------------------

    def move(self, arena: Arena):

        # Animazione
        self._frame_counter += 1
        self._frame_counter %= len(self._frames) * self._animation_speed

        # Collisioni
        for other in arena.actors():
            if other is self:
                continue

            # Se colpisce uno zombie → uccidi lo zombie e la fiaccola scompare (solo il primo zombie)
            if other.__class__.__name__ == "Zombie" and check_collision(self, other):
                other.hit(arena)
                arena.kill(self)
                return

            # Se colpisce un ostacolo (lapide o piattaforma) → genera Flame e scompare
            if type(other).__name__ in ("Gravestone", "Platform") and check_collision(self, other):
                arena.spawn(Flame((self._x, self._y)))
                arena.kill(self)
                return

        # Movimento orizzontale
        self._x += self._speed_x

        # Gravità
        self._falling_speed += TORCH_GRAVITY
        self._y += self._falling_speed

        # Rimbalzo sul terreno → genera Flame
        if self._y >= GROUND_H:
            arena.spawn(Flame((self._x, GROUND_H)))  # la fiamma nasce al suolo
            arena.kill(self)
            return

        # Limiti arena: se esce dallo schermo la fiaccola viene rimossa
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

    def sprite_size(self) -> Point:
        return self._frame_size