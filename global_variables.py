ARENA_W, ARENA_H = 3584,240
FLOOR_H, PLATFORM_FLOOR_H, GROUND_H = 165, 80, 180
GRAVITY = 0.3
TORCH_GRAVITY = 0.1

# Percorsi
online_bg, online_sprites = "https://fondinfo.github.io/sprites/ghosts-goblins-bg.png", "https://fondinfo.github.io/sprites/ghosts-goblins.png"
offline_bg, offline_sprites = "public/ghosts-goblins-bg.png", "public/ghosts-goblins.png"
audio_path = "public/game_music.mp3"
throw_torch_path = "public/throw.mp3"
zombie_hit_path = "public/zombie_hit.mp3"
 
x_view, y_view = 0, 0 # Posizione di partenza
w_view, h_view = 600, ARENA_H  # Dimensione del canvas view


# Coordinate dei buchi (acqua), (x,width)
holes = [ (1699, 128), (1954,32), (2018,32), (2450, 32), (2706, 32)]
# Coordinate e dimensioni lapidi
gravestones = [
        [(1522, FLOOR_H), (16, 16)], [(1265, FLOOR_H), (18, 14)],
        [(1106, FLOOR_H - 2), (16, 16)], [(962, FLOOR_H - 2), (16, 16)],
        [(754, FLOOR_H - 2), (16, 16)], [(530, FLOOR_H - 2), (16, 16)],
        [(418, FLOOR_H), (16, 14)], [(242, FLOOR_H - 2), (16, 16)],
        [(50, FLOOR_H - 2), (16, 16)], [(770, PLATFORM_FLOOR_H), (17, 14)],
        [(866, PLATFORM_FLOOR_H), (16, 16)], [(962, PLATFORM_FLOOR_H), (16, 14)]
    ]

import g2d
def play_audio(path: str):

    '''
    Permette di emettere un effetto sonoro
    '''
    loop = True if path=="public/game_music.mp3" else False # La musica di gioco e' in loop mentre gli altri effetti sonori no
    try:    
        g2d.play_audio(path, loop)
    except:
        pass