#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from random import randrange, randint
import g2d

from actor import Arena, check_collision
from arthur import Arthur
from gravestone import Gravestone
from platform import Platform
from zombie import Zombie
from torch import Torch
from flame import Flame
from hole import Hole

from global_variables import (
    ARENA_W, ARENA_H, x_view, y_view, w_view, h_view,
    FLOOR_H, PLATFORM_FLOOR_H, GRAVITY,
    online_bg, online_sprites
)

# flag per indicare che Arthur sta sopra un buco e quindi
# bisogna ignorare le piattaforme sotto di lui
ignore_platforms_under = False


# --------------------------------------------------------
# FUNZIONI DI SUPPORTO
# --------------------------------------------------------

def check_obstacle_collision(a):
    global ignore_platforms_under
    if ignore_platforms_under:
        # Arthur è sopra un buco: non considerare collisioni con le piattaforme
        return
    
    ax, ay, aw, ah = arthur.pos() + arthur.size()
    gx, gy, gw, gh = a.pos() + a.size()

    if check_collision(arthur, a):
        feet_y = ay + ah
        top_y = gy

        # Se Arthur è sopra una gravestone o una platform (in caduta); 6 pixel di tolleranza dovuti al tick
        if abs(feet_y - top_y) < 6 and arthur._falling_speed >= 0:
            arthur._isfloating = True
            arthur._y = top_y - ah # Imposto Arthur sul tetto
            arthur._jumping = False
            arthur._falling_speed = 0 # Azzero la gravità
            arthur._lateral_collision = False
        else:
            # Gravestone: collisione laterale
            if type(a).__name__ == "Gravestone":
                if ax + aw > gx and ax < gx + gw:
                    arthur._lateral_collision = True
            else:
                arthur._lateral_collision = False  # Le piattaforme non bloccano lateralmente


# --------------------------------------------------------
# GAME LOOP
# --------------------------------------------------------

def tick():
    global x_view, y_view, ignore_platforms_under

    g2d.clear_canvas()
    g2d.draw_image(online_bg, pos=(0, 0), clip_pos=(x_view + 2, y_view + 10), clip_size=(w_view, h_view))

    # Vista centrata su Arthur
    bx, by = arthur.pos()
    arena_w, arena_h = arena.size()
    x_view = bx - w_view // 2
    y_view = by - h_view // 2

    # Mantiene la vista entro i limiti dell'arena
    x_view = max(0, min(x_view, arena_w - w_view))
    y_view = max(0, min(y_view, arena_h - h_view))

    # Calcolo la posizione relativa allo schermo
    screen_pos = (bx - x_view, by - y_view)
    
    if arthur in arena.actors():
        g2d.draw_image(online_sprites, screen_pos, arthur.sprite(), arthur.sprite_size())
    else:
        g2d.set_color((200,50,60))
        g2d.draw_text("GAME OVER",(x_view / 2, ARENA_H / 2), 50)

    # Spawn casuale dei zombie
    if randrange(50) == 1:
        spawn_x = arthur._x + randint(-200, 200)
        direction = "left" if spawn_x >= arthur._x else "right" # Direzione zombie in base alla pos di Arthur
        arena.spawn(Zombie(spawn_x, direction))

    # Reset flag
    arthur._lateral_collision = False
    arthur._isfloating = False

    # Controllo buchi
    arthur_over_hole = False
    ax, ay = arthur.pos()
    aw, ah = arthur.size()

    for h in arena.actors():
        if isinstance(h, Hole):
            hx, hy = h.pos()
            hw, hh = h.size()

            # Arthur
            if ax + aw > hx and ax < hx + hw:      # orizzontalmente
                if ay + ah <= hy:                 # piedi sopra l'apertura
                    arthur_over_hole = True

            # Zombie
            for z in arena.actors():
                if isinstance(z, Zombie):
                    zx, zy = z.pos()
                    zw, zh = z.size()

                    if zx + zw > hx and zx < hx + hw:
                        if zy + zh <= hy:
                            # Zombie cade
                            z._falling_speed += GRAVITY
                            z._y += z._falling_speed

    if arthur_over_hole:
        arthur._isfloating = False
        arthur._jumping = False
        ignore_platforms_under = True
    else:
        ignore_platforms_under = False


    # Ciclo sugli attori
    for a in arena.actors():
        if not isinstance(a, (Platform, Gravestone, Arthur, Torch, Flame, Hole)):
            actor_x, actor_y = a.pos()
            screen_actor_pos = (actor_x - x_view, actor_y - y_view)
            g2d.draw_image(online_sprites,
                           screen_actor_pos, a.sprite(), a.sprite_size())

        # Collisione con gli ostacoli (Gravestone o Platform)
        if isinstance(a, Platform) and not isinstance(a, Hole):
            check_obstacle_collision(a)

        if isinstance(a, Gravestone):
            check_obstacle_collision(a)

        if isinstance(a, (Torch, Flame)):
            actor_x, actor_y = a.pos()
            screen_actor_pos = (actor_x - x_view, actor_y - y_view)
            g2d.draw_image(online_sprites, screen_actor_pos, a.sprite(), a.sprite_size())


    arena.tick(g2d.current_keys())


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------

def main():
    global arena, arthur

    arena = Arena((ARENA_W, ARENA_H))
    arthur = Arthur((1600, FLOOR_H))
    arena.spawn(arthur)

    # Coordinate Platform e Lapidi
    holes = [
        [(1699, FLOOR_H), (128,50)], [(1954, FLOOR_H), (32,47)], [(2018, FLOOR_H), (32,43)], 
        [(2450, FLOOR_H), (32,42)], [(2706, FLOOR_H), (32,42)]
    ]

    gravestones = [
        [(1522, FLOOR_H), (16, 16)], [(1265, FLOOR_H), (18, 14)],
        [(1106, FLOOR_H - 2), (16, 16)], [(962, FLOOR_H - 2), (16, 16)],
        [(754, FLOOR_H - 2), (16, 16)], [(530, FLOOR_H - 2), (16, 16)],
        [(418, FLOOR_H), (16, 14)], [(242, FLOOR_H - 2), (16, 16)],
        [(50, FLOOR_H - 2), (16, 16)], [(770, PLATFORM_FLOOR_H), (17, 14)],
        [(866, PLATFORM_FLOOR_H), (16, 16)], [(962, PLATFORM_FLOOR_H), (16, 14)]
    ]
    
    arena.spawn(Platform((610, FLOOR_H - 62), (527, 30))) # Platform fluttuante

    [arena.spawn(Hole(p[0], p[1])) for p in holes]   

    [arena.spawn(Gravestone(g[0], g[1])) for g in gravestones] # List comprehension che itera le lapidi e aggiunge all'arena

    g2d.init_canvas((w_view, h_view), scale=2) # Scale 2 aumenta lo Zoom
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()