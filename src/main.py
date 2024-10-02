import json
import os
from random import randint

import pygame
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Rutas y archivos
SCORES_FILE = "scores.json"


# Funciones auxiliares
def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as file:
            return json.load(file)
    return []


def save_score(new_score):
    scores = load_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:10]  # Mantener solo el top 10
    with open(SCORES_FILE, "w") as file:
        json.dump(scores, file)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Menú principal
def main_menu():
    font = pygame.font.Font(None, 74)
    menu = True
    while menu:
        screen.fill(BLACK)
        draw_text(
            "Bullet Game", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4
        )
        draw_text(
            "1. Iniciar Juego",
            font,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        )
        draw_text(
            "2. Ver Top 10",
            font,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
        )
        draw_text(
            "3. Salir", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    game()
                if event.key == K_2:
                    show_top_scores()
                if event.key == K_3:
                    pygame.quit()
                    exit()


# Pantalla de Top Scores
def show_top_scores():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    scores = load_scores()

    showing_scores = True
    while showing_scores:
        screen.fill(BLACK)
        draw_text(
            "Top 10 Scores", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6
        )

        for i, score in enumerate(scores):
            draw_text(
                f"{i + 1}. {score}",
                small_font,
                WHITE,
                screen,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 4 + 50 * (i + 1),
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    showing_scores = False


# Juego principal
def game():
    player = pygame.Rect(
        SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 50, 50
    )  # Rectángulo para la nave del jugador
    player_speed = 5

    enemies = []
    bullets = []
    enemy_timer = 0
    score = 0
    clock = pygame.time.Clock()

    playing = True
    start_time = pygame.time.get_ticks()

    while playing:
        screen.fill(BLACK)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player.left > 0:
            player.move_ip(-player_speed, 0)
        if keys[K_RIGHT] and player.right < SCREEN_WIDTH:
            player.move_ip(player_speed, 0)
        if keys[K_SPACE]:  # Disparar
            if len(bullets) < 5:  # Limitar el número de balas
                bullets.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))

        # Generar enemigos
        if (
            pygame.time.get_ticks() - enemy_timer > 1000
        ):  # Un nuevo enemigo cada segundo
            enemies.append(pygame.Rect(randint(0, SCREEN_WIDTH - 50), 0, 50, 50))
            enemy_timer = pygame.time.get_ticks()

        # Mover enemigos
        for enemy in enemies[:]:
            enemy.move_ip(0, 5)
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # Mover balas
        for bullet in bullets[:]:
            bullet.move_ip(0, -10)
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Detectar colisiones
        for enemy in enemies[:]:
            if player.colliderect(enemy):
                playing = False  # Fin del juego si colisiona con el jugador
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)

        # Dibujar jugador, enemigos y balas
        pygame.draw.rect(screen, WHITE, player)
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)
        for bullet in bullets:
            pygame.draw.rect(screen, (0, 255, 0), bullet)

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar FPS
        clock.tick(60)

    # Fin de la partida
    end_time = pygame.time.get_ticks()
    score = (end_time - start_time) // 1000  # Calcular el tiempo de vida
    save_score(score)
    game_over_menu(score)


# Menú de fin de juego
def game_over_menu(score):
    font = pygame.font.Font(None, 74)
    over = True
    while over:
        screen.fill(BLACK)
        draw_text(
            f"Game Over", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3
        )
        draw_text(
            f"Score: {score}",
            font,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        )
        draw_text(
            "1. Reiniciar",
            font,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
        )
        draw_text(
            "2. Menú principal",
            font,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 200,
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    game()
                if event.key == K_2:
                    over = False


# Ejecutar el menú principal al iniciar el juego
main_menu()
