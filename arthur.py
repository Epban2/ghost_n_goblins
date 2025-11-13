from actor import Actor, Arena, Point

from global_variables import FLOOR_H, GRAVITY


class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._speed = 3
        
        self._falling_speed = 0 #per la gravita
        
        #Flag e contatori
        self._lateral_collision = False #viene impostato su true se scontra zombie/gravestones nel tick di main
        self._isfloating = False

        self._walking = False
        self._crouching = False
        self._jumping = False
        self._walking_counter = 0
        self._jumping_counter = 0
        self._watching = "right" #left
        
        #idle sprite, size
        self._idle_rigth_sprite = (6, 43)
        self._idle_left_sprite = (486, 43)
        self._idle_size = (20, 31)

        #walking sprite, size
        self._walking_rigth_sprite = [(40,44),(66, 42),(88,43),(109,43)]
        self._walking_left_sprite = [(449,44),(427, 42),(405,43),(379,43)]
        self._walking_size =   [(23,28), (19,32),(19,31),(24,29)]

        #crouch sprite, size
        self._crouch_rigth_sprite = (222, 52 )
        self._crouch_left_sprite = (267, 52)
        self._crouch_size = (22, 22)

        #jump sprite, size
        self._jump_rigth_sprite = [(144,29),(180,29)]
        self._jump_left_sprite = [(336,29),(305,29)]
        self._jump_size = [(32,27),(27, 26)]
        
        

    def move(self, arena: Arena):
        #azzera tutti i flag e controlla i tasti
        self._walking = False
        self._crouching = False
        
        keys = arena.current_keys()
        keys = arena.current_keys()
        if "ArrowUp" in keys and (self._y == FLOOR_H or self._isfloating) : # se salta ed e' a terra 
            self._jumping = True
            self._falling_speed = -4.4 #coefficiente del salto
        elif "ArrowDown" in keys:
            self._crouching = True
        
        #controllo degli input (anche in funzione delle collisioni)
        if (self._lateral_collision and self._watching == "right") or not self._lateral_collision: #se è contro la lapide ma va in direzione opposta (alla parete della gravestone)
            if "ArrowLeft" in keys:
                self._x -= self._speed
                self._watching = "left"
                self._walking = True
        
        if (self._lateral_collision and self._watching == "left") or not self._lateral_collision:
            if "ArrowRight" in keys:
                self._x += self._speed
                self._watching = "right"
                self._walking = True

        # Gestione gravita'
        # se sta appoggiato su qualcosa oppure non e' in aria la gravita' percepita e' 0
        if self._isfloating and not self._jumping:
            self._falling_speed = 0
        else:
            # se sta saltando (anche dalla piattaforma) o è in aria, applica la gravità
            self._falling_speed += GRAVITY

        self._y+=self._falling_speed
    
        # Gestione pavimento
        if self._y >= FLOOR_H:
            self._y = FLOOR_H
            self._falling_speed = 0
            self._jumping = False #una volta atterrato azzero il flag

        # Controllo degli estremi del canvas
        aw, ah = arena.size()
        self._x = min(max(self._x, 0), aw - self._w)  # clamp
        self._y = min(max(self._y, 0), ah - self._h)  # clamp

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
        sprite = None
        if self._watching  == "right":
            if self._jumping: #salta
                sprite = self._jump_rigth_sprite[self._jumping_counter//5] 
            elif self._walking: #cammina
                sprite = self._walking_rigth_sprite[self._walking_counter//4] #Faccio //4 cosi' ogni sprite dura per 4frame e quindi la passeggiata sembra piu' fluida
                self._walking_counter +=1
            elif self._crouching: #crouch
                sprite = self._crouch_rigth_sprite 
                self._jumping_counter +=1
            else: #non fa niente, sta fermo
                sprite = self._idle_rigth_sprite
                self._walking_counter = 0
                
        else:  #guarda sinistra
            if self._jumping: #salta
                sprite = self._jump_left_sprite[self._jumping_counter//5]
            elif self._walking: #cammina
                sprite = self._walking_left_sprite[self._walking_counter//4]
                self._walking_counter +=1
            elif self._crouching: #crouch
                sprite = self._crouch_left_sprite 
                self._jumping_counter +=1
            else: #idle
                sprite = self._idle_left_sprite
                self._walking_counter = 0
                
        
        self._walking_counter%=len(self._walking_rigth_sprite)*4 #Poiché ho incrementato l'indice, mi assicuro che rientri nell'intervallo (moltiplico inoltre per 4 == frame per sprite)
        self._jumping_counter%=len(self._jump_rigth_sprite)*5 #Poiché ho incrementato l'indice, mi assicuro che rientri nell'intervallo (moltiplico inoltre per 4 == frame per sprite)
        
        return sprite


    def sprite_size(self) -> Point:
        size = None

        if self._jumping: #salta
            size = self._jump_size[self._jumping_counter//5]
        elif self._walking: #se sta camminando 
            size = self._walking_size[self._walking_counter//4]
        elif self._crouching: #se e' in ginocchio
            size = self._crouch_size
             
        else:
            size = self._idle_size
    
        return size