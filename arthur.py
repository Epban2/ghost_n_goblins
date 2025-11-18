from actor import Actor, Arena, Point, check_collision
from torch import Torch
from global_variables import FLOOR_H, GRAVITY
from zombie import Zombie


class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._speed = 3
        self._falling_speed = 0 # Gravità

        # Flag e contatori
        self._lateral_collision = False # True se collide con ostacoli (Gravestone o Zombie)
        self._isfloating = False
        self._walking = False
        self._crouching = False
        self._jumping = False
        self._watching = "right"
        self._walking_counter = 0
        self._jumping_counter = 0
        self._torch_cooldown = 0

        # Sprite e dimensioni
        self._idle_rigth_sprite = (6, 43)
        self._idle_left_sprite = (486, 43)
        self._idle_size = (20, 31)

        self._walking_rigth_sprite = [(40, 44), (66, 42), (88, 43), (109, 43)]
        self._walking_left_sprite = [(449, 44), (427, 42), (405, 43), (379, 43)]
        self._walking_size = [(23, 28), (19, 32), (19, 31), (24, 29)]

        self._crouch_rigth_sprite = (222, 52)
        self._crouch_left_sprite = (267, 52)
        self._crouch_size = (22, 22)

        self._jump_rigth_sprite = [(144, 29), (180, 29)]
        self._jump_left_sprite = [(336, 29), (305, 29)]
        self._jump_size = [(32, 27), (27, 26)]

        self._fall_rigth_sprite = (180, 29)
        self._fall_left_sprite = (306, 29)
        self._fall_size = (27, 26)


    # -----------------------------------------------------

    def move(self, arena: Arena):
        # Controllo se dve terminare il gioco
        # for actor in arena.actors():
        #     if isinstance(actor, Zombie):
        #         if check_collision(self, actor):
        #             self.hit(arena) #END GAME

        #
        # Azzera tutti i flag e controlla i tasti
        self._walking = False
        self._crouching = False

        keys = arena.current_keys()

        # Controllo del salto
        if "ArrowUp" in keys and (self._y == FLOOR_H or self._isfloating):
            self._jumping = True
            self._falling_speed = -4.4 # Coefficiente del salto

        elif "ArrowDown" in keys:
            self._crouching = True

        # Movimento orizzontale
        if (self._lateral_collision and self._watching == "right") or not self._lateral_collision:
            if "ArrowLeft" in keys:
                self._x -= self._speed
                self._watching = "left"
                self._walking = True

        if (self._lateral_collision and self._watching == "left") or not self._lateral_collision:
            if "ArrowRight" in keys:
                self._x += self._speed
                self._watching = "right"
                self._walking = True

        # Lancio fiaccola
        if "Spacebar" in keys and self._torch_cooldown == 0:
            direction = self._watching
            arena.spawn(Torch((self._x, self._y), direction))
            self._torch_cooldown = 10

        # Gravità
        if self._isfloating and not self._jumping:
            self._falling_speed = 0 # Se appoggiato imposto a 0 la gravità
        else:
            self._falling_speed += GRAVITY # Altrimenti se sta saltanto la applico

        self._y += self._falling_speed

        # Pavimento
        if self._y >= FLOOR_H:
            self._y = FLOOR_H
            self._falling_speed = 0
            self._jumping = False # Atterrato

        if self._torch_cooldown > 0:
            self._torch_cooldown -= 1

        # Limiti del canvas
        aw, ah = arena.size()
        self._x = min(max(self._x, 0), aw - self._w)
        self._y = min(max(self._y, 0), ah - self._h)

    # -----------------------------------------------------

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    # -----------------------------------------------------

    def sprite(self) -> Point:
        sprite = None

        if self._watching == "right":
            if self._jumping and self._falling_speed > 0:
                return self._fall_rigth_sprite
            elif self._jumping:
                sprite = self._jump_rigth_sprite[self._jumping_counter // 5]
            elif self._walking:
                sprite = self._walking_rigth_sprite[self._walking_counter // 4]
                self._walking_counter += 1
            elif self._crouching:
                sprite = self._crouch_rigth_sprite
                self._jumping_counter += 1
            else:
                sprite = self._idle_rigth_sprite
                self._walking_counter = 0
        else:
            if self._jumping and self._falling_speed > 0:
                return self._fall_left_sprite
            elif self._jumping:
                sprite = self._jump_left_sprite[self._jumping_counter // 5]
            elif self._walking:
                sprite = self._walking_left_sprite[self._walking_counter // 4]
                self._walking_counter += 1
            elif self._crouching:
                sprite = self._crouch_left_sprite
                self._jumping_counter += 1
            else:
                sprite = self._idle_left_sprite
                self._walking_counter = 0

        # Incremento l’indice, lo mantengo nel range e moltiplico per 4 (frame/sprite).
        self._walking_counter %= len(self._walking_rigth_sprite) * 4
        self._jumping_counter %= len(self._jump_rigth_sprite) * 5
        return sprite

    # -----------------------------------------------------

    def sprite_size(self) -> Point:
        if self._jumping and self._falling_speed > 0:
            return self._fall_size
        elif self._jumping:
            return self._jump_size[self._jumping_counter // 5]
        elif self._walking:
            return self._walking_size[self._walking_counter // 4]
        elif self._crouching:
            return self._crouch_size
        else:
            return self._idle_size
