from actor import Actor, Arena, Point, check_collision

class Flame(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 15, 15

        # Durata della fiamma (spec: 60 frame)
        self._lifetime = 60

        self._frames = [
            (210, 443),
            (229, 450),
            (210, 443),
            (229, 450)
        ]
        self._frame_size = (15, 15)

        self._frame_counter = 0
        self._animation_speed = 4

    # ---------------------------------------------------------

    def move(self, arena: Arena):
        # aggiornamento animazione
        self._frame_counter += 1
        self._frame_counter %= len(self._frames) * self._animation_speed

        self._lifetime -= 1
        if self._lifetime <= 0:
            arena.kill(self)
            return

        # controlla collisioni con tutti gli attori
        for other in arena.actors():
            if other is self:
                continue

            # se collide ed è uno zombie → uccidilo (la fiamma uccide tutti gli zombie che tocca)
            if other.__class__.__name__ == "Zombie":
                if check_collision(self, other):
                    other.hit(arena)

    # ---------------------------------------------------------

    def hit(self, arena: Arena):
        return  # La fiamma non viene distrutta quando viene colpita.

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        index = self._frame_counter // self._animation_speed
        return self._frames[index]

    def sprite_size(self) -> Point:
        return self._frame_size