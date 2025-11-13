from random import randint
from actor import Actor, Arena, Point
from global_variables import FLOOR_H, GRAVITY


class Zombie(Actor):
    def __init__(self, spawn_x, direction):
        self._x, self._y = spawn_x, FLOOR_H + 20
        self._direction = direction

        self._w, self._h = 20, 20
        self._speed = -1.5 if direction == "left" else 1.5
        self._distance = randint(150, 300)
        self._steps_done = 0 # Distanza percorsa
        self._falling_speed = 0 # Gravità

        # Flag e contatori
        self._iswalking = False
        self._isspawning = True # Generazione
        self._isdespawning = False
        self._walking_counter = 0
        self._spawning_counter = 0
        self._despawning_counter = 0

        # Sprite e dimensioni
        self._walking_left_sprite = [(585, 66), (610, 65), (631, 66)]
        self._walking_right_sprite = [(654, 66), (677, 65), (699, 66)]
        self._walking_size = [(22, 31), (19, 32), (21, 31)]

        self._spawning_left_sprite = [(512, 88), (533, 85), (562, 73)]
        self._spawning_right_sprite = [(725, 73), (748, 85), (778, 88)]
        self._spawning_size = [(16, 9), (25, 12), (19, 24)]

    # -----------------------------------------------------

    def move(self, arena: Arena):

        '''
        for other in arena.collisions():
            if isinstance(other, Ball):
                self.hit(arena)
        '''

        # Spawn
        if self._isspawning:
            self._spawning_counter += 1
            self._isspawning = (self._spawning_counter //
                                (14 * len(self._spawning_left_sprite))) == 0 # Controllo se è terminata l'animazione (14 frame per ogni immagine)
            if not self._isspawning: # Comincia a camminare
                self._iswalking = True

        elif self._iswalking:
            # Camminata
            if self._steps_done + abs(self._speed) < self._distance: # Controllo se ha già percorso la sua distanza
                self._x += self._speed
                self._steps_done += abs(self._speed)

                # Gravità
                self._falling_speed += GRAVITY
                self._y += self._falling_speed

                if self._y >= FLOOR_H:
                    self._y = FLOOR_H
                    self._falling_speed = 0

                aw, ah = arena.size()
                self._x = min(max(self._x, 0), aw - self._w)
                self._y = min(max(self._y, 0), ah - self._h)
            else:
                # Despawn terminato i passi
                self._iswalking = False
                self._isdespawning = True

        elif self._isdespawning:
            self._despawning_counter += 1
            self._isdespawning = (self._despawning_counter //
                                  (14 * len(self._spawning_left_sprite))) == 0 # Controllo se è terminata l'animazione
        else:
            # Se ha terminato le sue interazioni
            arena.kill(self)

    # -----------------------------------------------------

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    # -----------------------------------------------------

    def sprite(self) -> Point:

        sprite = (2,20) #Inizializzo per sicurezza

        if self._direction == "left":
            if self._isspawning:
                sprite = self._spawning_left_sprite[self._spawning_counter // 14]
                self._spawning_counter += 1
                self._y -= 1
            elif self._iswalking:
                sprite = self._walking_left_sprite[self._walking_counter // 4]
                self._walking_counter += 1
            elif self._isdespawning:
                sprite = self._spawning_left_sprite[::-1][self._despawning_counter // 14]
                self._despawning_counter += 1
                self._y += 1
        else: # Destra
            if self._isspawning:
                sprite = self._spawning_right_sprite[self._spawning_counter // 14]
                self._spawning_counter += 1
                self._y -= 1
            elif self._iswalking:
                sprite = self._walking_right_sprite[self._walking_counter // 4]
                self._walking_counter += 1
            elif self._isdespawning:
                sprite = self._spawning_right_sprite[::-1][self._despawning_counter // 14] # Inverto la lista poiché mi serve l'animazione inversa dello spawn
                self._despawning_counter += 1
                self._y += 1

        # # Controllo se è terminata l'animazione (4 frame per sprite)
        self._walking_counter %= len(self._walking_right_sprite) * 4
        self._spawning_counter %= len(self._spawning_right_sprite) * 14
        self._despawning_counter %= len(self._spawning_right_sprite) * 14
        return sprite

    # -----------------------------------------------------

    def sprite_size(self) -> Point:

        size = (1,1) # Inizializzo per sicurezza

        if self._direction == "left":
            if self._isspawning:
                return self._spawning_size[self._spawning_counter // 14]
            elif self._iswalking:
                return self._walking_size[self._walking_counter // 4]
            elif self._isdespawning:
                return self._spawning_size[::-1][self._despawning_counter // 14]
        else:
            if self._isspawning:
                return self._spawning_size[self._spawning_counter // 14]
            elif self._iswalking:
                return self._walking_size[self._walking_counter // 4]
            elif self._isdespawning:
                return self._spawning_size[::-1][self._despawning_counter // 14]
        return size