import pygame
import sys
import random
from card import Card
from config import *

# -----------------------------------------
def load_image(path):
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (IMAGE_WIDTH * 2, IMAGE_WIDTH))
        return img
    except pygame.error as e:
        print(f"Erro ao carregar {path}: {e}")
        return None

def create_image_list():
    orig = [
        "imagens/original/original_seno_100Hz.png",
        "imagens/original/original_seno_200Hz.png",
        "imagens/original/original_seno_500Hz.png",
        "imagens/original/original_seno_1000Hz.png",
        "imagens/original/original_seno_5000Hz.png"
    ]
    amost = [
        "imagens/amostras/amostras_seno_100Hz.png",
        "imagens/amostras/amostras_seno_200Hz.png",
        "imagens/amostras/amostras_seno_500Hz.png",
        "imagens/amostras/amostras_seno_1000Hz.png",
        "imagens/amostras/amostras_seno_5000Hz.png"
    ]
    recon = [
        "imagens/reconstruido/reconstruido_seno_100Hz.png",
        "imagens/reconstruido/reconstruido_seno_200Hz.png",
        "imagens/reconstruido/reconstruido_seno_500Hz.png",
        "imagens/reconstruido/reconstruido_seno_1000Hz.png",
        "imagens/reconstruido/reconstruido_seno_5000Hz.png"
    ]
    images = []
    for i in range(len(orig)):
        o = load_image(orig[i])
        a = load_image(amost[i])
        r = load_image(recon[i])
        if o and a and r:
            images.append((o, a, r))
    return images

def create_board(images):
    Card.instances.clear()
    n_colunas = len(images)
    largura_img = images[0][0].get_width()
    altura_img = images[0][0].get_height()
    n_linhas = 3

    espaco_x = (WINDOW_WIDTH - n_colunas * largura_img) / (n_colunas + 1)
    espaco_y = (WINDOW_HEIGHT - n_linhas * altura_img) / (n_linhas + 1)

    linhas = [
        [(img[0], set_id) for set_id, img in enumerate(images)],
        [(img[1], set_id) for set_id, img in enumerate(images)],
        [(img[2], set_id) for set_id, img in enumerate(images)]
    ]
    for linha in linhas:
        random.shuffle(linha)

    for row in range(n_linhas):
        for col in range(n_colunas):
            img, set_id = linhas[row][col]
            x = espaco_x + col * (largura_img + espaco_x)
            y = espaco_y + row * (altura_img + espaco_y)
            Card(x, y, img, set_id, row)

# -----------------------------------------
hide_timer = None
game_state = "showing"  # showing, playing
show_start_time = None

def handle_click(pos):
    global hide_timer
    if hide_timer or game_state != "playing":
        return

    for card in Card.instances:
        if card.rect.collidepoint(pos) and not card.revealed and card not in Card.correct:
            if any(c.row == card.row for c in Card.guesses):
                return
            card.start_fade_in()
            Card.guesses.append(card)
            break

    if len(Card.guesses) == 3:
        set_ids = {c.set_id for c in Card.guesses}
        rows = {c.row for c in Card.guesses}
        if len(set_ids) == 1 and len(rows) == 3:
            Card.correct.extend(Card.guesses)
            Card.guesses.clear()
        else:
            hide_timer = pygame.time.get_ticks() + HIDE_DELAY

def update_hide_timer():
    global hide_timer
    if hide_timer and pygame.time.get_ticks() >= hide_timer:
        for c in Card.guesses:
            if c not in Card.correct:
                c.start_fade_out()
        Card.guesses.clear()
        hide_timer = None

# -----------------------------------------
def draw_menu(screen, mouse_pos):
    screen.fill((255, 255, 255))
    font_title = pygame.font.Font("OpenSans-Light.ttf", 60)
    font_button = pygame.font.Font("OpenSans-Light.ttf", 40)

    title = font_title.render("Jogo da Memória - Nyquist", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
    screen.blit(title, title_rect)

    # Botões
    play_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 60)
    quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 400, 200, 60)

    for rect, text in [(play_rect, "Jogar"), (quit_rect, "Sair")]:
        color = (0, 150, 255) if rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surf = font_button.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    return play_rect, quit_rect

# -----------------------------------------
def main():
    global show_start_time, game_state
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Jogo da Memória - Nyquist")
    clock = pygame.time.Clock()

    state = "menu"
    images = create_image_list()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_btn.collidepoint(mouse_pos):
                        create_board(images)
                        for card in Card.instances:
                            card.start_fade_in()
                        show_start_time = pygame.time.get_ticks()
                        game_state = "showing"
                        state = "game"
                    elif quit_btn.collidepoint(mouse_pos):
                        running = False

            elif state == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    handle_click(event.pos)

        if state == "menu":
            play_btn, quit_btn = draw_menu(screen, mouse_pos)

        elif state == "game":
            font = pygame.font.Font("OpenSans-Light.ttf", 36)
            text = font.render("Clique para revelar cartas", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 40))
            screen.blit(text, text_rect)

            if game_state == "showing":
                if pygame.time.get_ticks() - show_start_time >= SHOW_TIME:
                    for card in Card.instances:
                        card.start_fade_out()
                    game_state = "playing"

            update_hide_timer()

            for card in Card.instances:
                card.update()
                card.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
