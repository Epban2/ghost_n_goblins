from random import randint
from actor import Actor, Arena, Point
from global_variables import FLOOR_H, GRAVITY, holes


class Zombie(Actor):
    def __init__(self, spawn_x, direction):
        self._x, self._y = spawn_x, FLOOR_H + 20
        self._direction = direction

        self._w, self._h = 20, 20
        self._speed = -0.8 if direction == "left" else 0.8
        self._distance = randint(150, 300)
        self._steps_done = 0 # Distanza percorsa
        self._falling_speed = 0 # Gravità

        # Flag e contatori
        self._iswalking = False
        self._isspawning = True # Generazione
        self._isdespawning = False
        self._is_falling = False
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


        # controllo se gli zombie cadono nell'acqua
        for hole in holes:
            if (hole[0] < self._x + self._w*2 and self._x < hole[0] + hole[1]) and self._y <= FLOOR_H + 3: #controllo se si trova in mezzo ai buchi
                self._is_falling = True                            #h+3 è la tolleranza di y

        if self._is_falling:
            self._falling_speed += GRAVITY # Altrimenti se sta saltanto la applico
            self._y += self._falling_speed

        if self._y>=220: #se è caduto nell'acqua,  muore
            self.hit(arena)
       
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