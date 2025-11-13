from actor import Actor, Arena, Point
from random import randint

from global_variables import FLOOR_H, GRAVITY


class Zombie(Actor):
    def __init__(self, spawn_x, direction):
        self._x, self._y = spawn_x, FLOOR_H + 20 #poiché lo spawn parte da piuù in basso...
        self._direction = direction #left o right

        self._w, self._h = 20, 20

        if self._direction == "left":
            self._speed = -1.5
        else:
            self._speed = 1.5

        self._distance = randint(150,300) #Percorre una distanza che va da 150 a 300
        self._steps_done = 0 #distanza percorsa
        self._falling_speed = 0 #per la gravita
        
        #Flag e contatori
        self._iswalking = False
        self._isspawning = True #Inizializzo a vero la generazione (per l'animazione)        
        self._isdespawning = False

        self._walking_counter = 0
        self._spawning_counter = 0
        self._despawning_counter = 0
                
        #walking sprite, size
        self._walking_left_sprite =  [(585,66), (610, 65), (631,66)]
        self._walking_right_sprite = [(654,66), (677, 65), (699,66)]
        self._walking_size =         [(22,31), (19,32), (21,31)]

        #spawn sprite, size
        self._spawning_left_sprite =  [(512,88), (533,85), (562,73)]
        self._spawning_right_sprite = [(725,73), (748,85), (778,88)]
        self._spawning_size =         [(16,9), (25,12), (19,24)]

        
    """
    """   
    def move(self, arena: Arena):
#        for other in arena.collisions():
#            if isinstance(other, Ball):
#                self.hit(arena)

        #spawn
        if self._isspawning:
            self._spawning_counter += 1
            self._isspawning = (self._spawning_counter // (14*len(self._spawning_left_sprite))) == 0 #per determinare se è terminata l'animazione di spawn (14 frame per ogni immagine (14*3))
            if not self._isspawning: #se ha smesso l'animazione comincia a camminare
                self._iswalking = True
        elif self._iswalking:
            #camminata
            if self._steps_done + abs(self._speed) < self._distance: #controllo se ha già percorso la sua distanza
                self._x += self._speed
                self._steps_done += abs(self._speed)
                
                #gravita
                self._falling_speed += GRAVITY
                self._y+=self._falling_speed
            

                if self._y >= FLOOR_H:
                    self._y = FLOOR_H
                    self._falling_speed = 0

                aw, ah = arena.size()
                self._x = min(max(self._x, 0), aw - self._w)  # clamp
                self._y = min(max(self._y, 0), ah - self._h)  # clamp
                
            else: #terminato i passi, despawn
                self._iswalking = False #
                self._isdespawning = True
        elif self._isdespawning:
            self._despawning_counter += 1
            self._isdespawning = (self._despawning_counter // (14*len(self._spawning_left_sprite))) == 0 #per determinare se è terminata l'animazione di spawn (14 frame per ogni immagine (14*3))

        else: #se tutti i flag sono spenti significa che ha terminato le interazioni
            arena.kill(self)

        #Applico la gravita' sempre
        


    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    """
    Vengono effettuati più controlli sulla direzione, movimento (true/false)
    """
    def sprite(self) -> Point:
        sprite = (2,20) #inizializzo per sicurezza

        if self._direction == "left":
            if self._isspawning: #spawnando
                sprite = self._spawning_left_sprite[self._spawning_counter//14]
                self._spawning_counter+=1
                self._y -= 1
            elif self._iswalking: #camminando
                sprite = self._walking_left_sprite[self._walking_counter//4]
                self._walking_counter+=1
            elif self._isdespawning: #despawnando
                sprite = self._spawning_left_sprite[::-1][self._despawning_counter//14]
                self._despawning_counter+=1
                self._y += 1
            
        else: #verso destra
            if self._isspawning: #spawnando
                sprite = self._spawning_right_sprite[self._spawning_counter//14]
                self._spawning_counter+=1
                self._y -= 1    
            elif self._iswalking: #cammiando
                sprite = self._walking_right_sprite[self._walking_counter//4]
                self._walking_counter+=1
            elif self._isdespawning: #despawn
                sprite = self._spawning_right_sprite[::-1][self._despawning_counter//14] #inverto la lista poiché mi serve l'animazione inversa dello spawn
                self._despawning_counter+=1
                self._y += 1


        self._walking_counter%=len(self._walking_right_sprite)*4 #Poiché ho incrementato l'indice, mi assicuro che rientri nell'intervallo (moltiplico inoltre per 4 == frame per sprite)
        self._spawning_counter%=len(self._spawning_right_sprite)*14 #Poiché ho incrementato l'indice, mi assicuro che rientri nell'intervallo (moltiplico inoltre per 4 == frame per sprite)
        self._despawning_counter%=len(self._spawning_right_sprite)*14 #Poiché ho incrementato l'indice, mi assicuro che rientri nell'intervallo (moltiplico inoltre per 4 == frame per sprite)


        return sprite


    def sprite_size(self) -> Point:
        size = (1,1)#inizializzo per sicurezza

        if self._direction == "left":
            if self._isspawning:
                size = self._spawning_size[self._spawning_counter//14]
            elif self._iswalking: #camminata
                size = self._walking_size[self._walking_counter//4]
            elif self._isdespawning: #despawn
                size = self._spawning_size[::-1][self._despawning_counter//14]

        else: #destra
            if self._isspawning:
                size = self._spawning_size[self._spawning_counter//14]
            elif self._iswalking:
                size = self._walking_size[self._walking_counter//4]
            elif self._isdespawning: #despawn
                size = self._spawning_size[::-1][self._despawning_counter//14]

            
        return size
    