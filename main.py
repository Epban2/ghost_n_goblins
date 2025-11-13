#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from actor import Arena, check_collision
from random import randrange,randint
import g2d
from arthur import Arthur
from gravestone import Gravestone
from my_platform import Platform
from zombie import Zombie
from global_variables import ARENA_W, ARENA_H, x_view, y_view, w_view, h_view, FLOOR_H, PLATFORM_FLOOR_H
from global_variables import online_bg, online_sprites, offline_bg, offline_sprites

def check_obstacle_collision(a):
    ax, ay, aw, ah = arthur.pos() + arthur.size()
    gx, gy, gw, gh = a.pos() + a.size()
    if check_collision(arthur, a):
        feet_y = ay + ah
        top_y = gy
        
        # controllo se si trova sopra gravestone o platform  ed è in caduta (dopo salto), (6 sono i pixel di tolleranza dovuti al tick)
        if abs(feet_y - top_y) < 6 and arthur._falling_speed >= 0:
            arthur._isfloating = True
            arthur._y = top_y - ah # imposto arthur suil tetto
            arthur._jumping = False
            arthur._falling_speed = 0 #azzero la gravità
            arthur._lateral_collision = False
        else:
            # se non sta saltando e sta collidendo una gravestone, imposto la collisione laterale
            if type(a).__name__ == 'Gravestone':
                if ax + aw > gx and ax < gx + gw:
                    arthur._lateral_collision = True
            else:
                arthur._lateral_collision = False  # Le piattaforme non bloccano lateralmente

##### GAME LOGIC
def tick():
    global x_view, y_view
    
    g2d.clear_canvas()
    
    g2d.draw_image(online_bg, pos=(0,0), clip_pos=(x_view+2, y_view+10), clip_size=(w_view, h_view))
    
    #vista
    bx, by = arthur.pos()
    arena_w, arena_h = arena.size()

    # Centra la  vista
    x_view = bx - w_view // 2
    y_view = by - h_view // 2

    #Mantiene la vista dentro i limiti
    x_view = max(0, min(x_view, arena_w - w_view))
    y_view = max(0, min(y_view, arena_h - h_view))
    ###    
    
    # Calcola la posizione relativa allo schermo
    screen_pos = (bx - x_view, by - y_view)
    g2d.draw_image(online_sprites, screen_pos, arthur.sprite(), arthur.sprite_size())
    
    
    if randrange(50) == 1: #probabilita' di spawn
        spawn_x = arthur._x + randint(-200,200) #max 200 dalla posizione di arthur
        direction = "left"
        if spawn_x < arthur._x: #se si trova alla sinistra di arthur deve andare verso destra
            direction = "right"
        arena.spawn(Zombie(spawn_x,direction))


    #Reset dei flag delle collisioni
    arthur._lateral_collision = False
    arthur._isfloating = False
    
    for a in arena.actors():
        if not isinstance(a, (Platform, Gravestone, Arthur)): #and not isinstance(a, Platform)
            actor_x, actor_y = a.pos()
            screen_actor_pos = (actor_x - x_view,  actor_y - y_view,)
            g2d.draw_image("https://fondinfo.github.io/sprites/ghosts-goblins.png", screen_actor_pos, a.sprite(), a.sprite_size())


        #COLLISIONE CON GLI OSTACOLI (lapidi o platform)
        if isinstance(a, (Gravestone, Platform)):
            check_obstacle_collision(a)

    arena.tick(g2d.current_keys())  # Game logic

####################
######  MAIN  ######
####################
def main():
    global arena, arthur

    arena = Arena((ARENA_W, ARENA_H))
    
    
    arthur = Arthur((900,55))
    arena.spawn(arthur)


    arena.spawn(Platform((610, FLOOR_H - 62), (527, 30))) #la platform è considerata come una striscia che fluttua, non un intero blocco


    gravestones = [[(1522, FLOOR_H),(16,16)],[(1265,FLOOR_H), (18,14)], [(1106,FLOOR_H-2), (16,16)], [(962,FLOOR_H-2), (16,16)], 
                   [(754,FLOOR_H-2), (16,16)],[(530,FLOOR_H-2), (16,16)],[(418,FLOOR_H), (16,14)],[(242,FLOOR_H-2), (16,16)],
                   [(50,FLOOR_H-2), (16,16)], [(770,PLATFORM_FLOOR_H), (17,14)], [(866,PLATFORM_FLOOR_H), (16,16)],[(962,PLATFORM_FLOOR_H), (16,14)]]

    for gravestone in gravestones:
        arena.spawn(Gravestone(gravestone[0], gravestone[1]))

    g2d.init_canvas((w_view, h_view),scale=2)
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()
