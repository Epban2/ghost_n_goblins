import pygame

# --- Inizializzazione ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# --- Variabili del giocatore ---
player_rect = pygame.Rect(400, 0, 30, 50)  # x, y, larghezza, altezza
player_velocity_y = 0  # Velocità verticale iniziale
GRAVITY = 0.3  # Valore dell'accelerazione di gravità

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Applica la gravità alla velocità
    player_velocity_y += GRAVITY

    # 2. Aggiorna la posizione Y del giocatore usando la sua velocità
    player_rect.y += player_velocity_y

    # --- Semplice controllo per non cadere fuori dallo schermo ---
    if player_rect.bottom > 600:
        player_rect.bottom = 600
        player_velocity_y = 0  # Ferma il giocatore quando tocca terra

    # --- Disegno ---
    screen.fill((0, 0, 0))  # Sfondo nero
    pygame.draw.rect(screen, (255, 0, 0), player_rect)  # Disegna il giocatore
    pygame.display.flip()

    clock.tick(60)  # Limita il gioco a 60 FPS

pygame.quit()