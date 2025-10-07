import pygame
import sys
import random

pygame.init()

# Colores
BACKGROUND = (255, 250, 255)
BUTTON_COLOR = (255, 204, 229)
HOVER_COLOR = (255, 153, 204)
TEXT_COLOR = (102, 0, 102)
ACCENT = (204, 255, 229)
WIN_COLOR = (153, 255, 153)
LOSE_COLOR = (255, 153, 153)
DRAW_COLOR = (204, 204, 255)

# Pantalla
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piedra, Papel o Tijera - Versión Kawaii")

# Fuentes
font = pygame.font.SysFont("Comic Sans MS", 48)
small_font = pygame.font.SysFont("Comic Sans MS", 28)

# Cargar imágenes
def load_image(path):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (120, 120))
    except:
        return None

img_piedra = load_image("assets/piedra.png")
img_papel = load_image("assets/papel.png")
img_tijera = load_image("assets/tijera.png")

images = {
    "piedra": img_piedra,
    "papel": img_papel,
    "tijera": img_tijera
}

# Estados del juego
choices = ["piedra", "papel", "tijera"]
player_choice = None
ai_choice = None
result = None
animation_frames = 0
ANIM_DURATION = 60  # frames

# Estadísticas
total_games = 0
wins = 0

clock = pygame.time.Clock()

def get_result(player, ai):
    if player == ai:
        return "empate"
    elif (player == "piedra" and ai == "tijera") or \
         (player == "papel" and ai == "piedra") or \
         (player == "tijera" and ai == "papel"):
        return "ganaste"
    else:
        return "perdiste"

def draw_text(text, size, color, x, y, center=True):
    f = pygame.font.SysFont("Comic Sans MS", size)
    s = f.render(text, True, color)
    rect = s.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(s, rect)

def draw_choice_button(x, y, choice, hover=False):
    color = HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.circle(screen, color, (x, y), 75)
    pygame.draw.circle(screen, TEXT_COLOR, (x, y), 75, 3)
    img = images[choice]
    if img:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    return pygame.Rect(x - 75, y - 75, 150, 150)

def draw_choices_ui():
    cx = WIDTH // 2
    cy = HEIGHT // 2 + 50
    spacing = 180
    buttons = {}
    for i, choice in enumerate(choices):
        x = cx + (i - 1) * spacing
        y = cy
        hover = pygame.Rect(x - 75, y - 75, 150, 150).collidepoint(pygame.mouse.get_pos())
        rect = draw_choice_button(x, y, choice, hover)
        buttons[choice] = rect
    return buttons

def draw_results():
    global wins, total_games

    draw_text("VS", 64, ACCENT, WIDTH // 2, HEIGHT // 2 - 140)

    # Mostrar elecciones
    player_img = images[player_choice]
    ai_img = images[ai_choice]
    if player_img:
        rect = player_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
        screen.blit(player_img, rect)
    if ai_img:
        rect = ai_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
        screen.blit(ai_img, rect)

    # Mostrar resultado
    color = DRAW_COLOR
    if result == "ganaste":
        color = WIN_COLOR
    elif result == "perdiste":
        color = LOSE_COLOR

    draw_text(result.upper(), 48, color, WIDTH // 2, HEIGHT // 2 + 150)

    # Botón reinicio
    restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, ACCENT, restart_rect, border_radius=15)
    pygame.draw.rect(screen, TEXT_COLOR, restart_rect, 2, border_radius=15)
    draw_text("Jugar de nuevo", 24, TEXT_COLOR, WIDTH // 2, HEIGHT - 55)
    return restart_rect

def draw_stats():
    prob_text = "Prob. a priori de ganar: 0.33"
    post_text = f"Partidas: {total_games} | Victorias: {wins} | Prob. a posteriori: {wins/total_games:.2f}" if total_games > 0 else "Partidas: 0 | Prob. a posteriori: --"
    draw_text(prob_text, 24, TEXT_COLOR, WIDTH // 2, 50)
    draw_text(post_text, 24, TEXT_COLOR, WIDTH // 2, 85)

# Bucle principal
running = True
while running:
    screen.fill(BACKGROUND)
    draw_stats()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_choice is None and animation_frames == 0:
                # Elección del jugador
                for choice, rect in draw_choices_ui().items():
                    if rect.collidepoint(event.pos):
                        player_choice = choice
                        ai_choice = random.choice(choices)
                        result = get_result(player_choice, ai_choice)
                        animation_frames = ANIM_DURATION
                        if result == "ganaste":
                            wins += 1
                        total_games += 1
                        break
            elif player_choice and animation_frames == 0:
                restart_rect = draw_results()
                if restart_rect.collidepoint(event.pos):
                    player_choice = None
                    ai_choice = None
                    result = None

    # Animación VS
    if player_choice and animation_frames > 0:
        draw_text("¡Preparados!", 48, ACCENT, WIDTH // 2, HEIGHT // 2 - 150)
        offset = 10 * (animation_frames % 2)
        if images[player_choice]:
            img = images[player_choice]
            rect = img.get_rect(center=(WIDTH // 2 - 200 + offset, HEIGHT // 2))
            screen.blit(img, rect)
        if images[ai_choice]:
            img = images[ai_choice]
            rect = img.get_rect(center=(WIDTH // 2 + 200 - offset, HEIGHT // 2))
            screen.blit(img, rect)
        animation_frames -= 1
    elif player_choice:
        draw_results()
    else:
        draw_text("Elige tu jugada", 36, TEXT_COLOR, WIDTH // 2, 140)
        draw_choices_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
