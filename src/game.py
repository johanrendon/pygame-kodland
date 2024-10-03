import json
import os
from pathlib import Path
from random import randint
from typing import List

import pygame

from meteor import Meteor
from player import Player
from settings import SCORES_FILE, WINDOW_HEIGHT, WINDOW_WIDTH
from star import Star


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space shooter")
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()

        # Import images
        self.meteor_surf: pygame.Surface = pygame.image.load(
            Path("../assets/images/meteor.png")
        )
        self.star_surf: pygame.Surface = pygame.image.load(
            Path("../assets/images/star.png")
        )
        for _ in range(20):
            Star(self.all_sprites, self.star_surf)

        self.player = Player(self.all_sprites)

        # import audio
        self.music = pygame.mixer.Sound(Path("../assets/audio/game_music.wav"))
        self.music.set_volume(0.4)
        self.music.play(loops=-1)

    def _display_score(self):
        text_surf = self.font.render(str(self.score), True, (240, 240, 240))
        text_rect = text_surf.get_frect(midtop=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            (240, 240, 240),
            text_rect.inflate(20, 10).move(0, -8),
            5,
            10,
        )

    def run(self):
        menu = True
        while menu:
            self.display_surface.fill("black")

            self._draw_text(
                "Bullet Game",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 4,
            )
            self._draw_text(
                "1. Iniciar Juego",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
            )

            self._draw_text(
                "2. Ver top 10",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 100,
            )

            self._draw_text(
                "3. Salir",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 200,
            )

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu = False
                        self._reset_game_state()
                        self._game()

                    if event.key == pygame.K_2:
                        self._show_scores()

                    if event.key == pygame.K_3:
                        self.running = False
                        menu = False

        pygame.quit()

    def _reset_game_state(self):
        self.score = 0
        self.running = True

        self.meteor_sprites.empty()
        self.laser_sprites.empty()

        self.player.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

    def _draw_text(
        self, text: str, font, color: str, surface: pygame.Surface, x: float, y: float
    ) -> None:
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

    def _game(self) -> None:
        meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(meteor_event, 200)

        while self.running:
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == meteor_event:
                    x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                    Meteor(
                        self.meteor_surf,
                        (x, y),
                        (self.all_sprites, self.meteor_sprites),
                    )
            # update
            self.all_sprites.update(dt, (self.all_sprites, self.laser_sprites))
            self._collisions()

            # draw the game
            self.display_surface.fill("#0d1b2a")
            self._display_score()
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

        self._menu_game_over()

    def _menu_game_over(self) -> None:
        self._save_scores()
        menu = True
        while menu:
            self.display_surface.fill("black")

            self._draw_text(
                "Game Over",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 4,
            )
            self._draw_text(
                f"Score {self.score}",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
            )

            self._draw_text(
                "1. Reiniciar",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 100,
            )

            self._draw_text(
                "2. Salir",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 200,
            )

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.menu = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu = False
                        self._reset_game_state()
                        self._game()

                    if event.key == pygame.K_2:
                        self.running = False
                        menu = False
        pygame.quit()

    def _collisions(self) -> None:
        collision_sprites: List[pygame.sprite.Sprite] = pygame.sprite.spritecollide(
            self.player, self.meteor_sprites, True, pygame.sprite.collide_mask
        )
        if collision_sprites:
            self.running = False

        for laser in self.laser_sprites:
            collide_sprites: List[pygame.sprite.Sprite] = pygame.sprite.spritecollide(
                laser, self.meteor_sprites, True
            )
            if collide_sprites:
                self.score += 1
                laser.kill()

    def _save_scores(self):
        scores = self._load_scores()
        scores.append(self.score)
        scores = sorted(scores, reverse=True)[:10]  # Mantener solo el top 10
        with open(SCORES_FILE, "w") as file:
            json.dump(scores, file)

    def _show_scores(self):
        scores = self._load_scores()

        show = True
        while show:
            self.display_surface.fill("black")
            self._draw_text(
                "Top 10 scores",
                self.font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 6,
            )

            # Mostrar los puntajes
            for index, score in enumerate(scores):
                self._draw_text(
                    f"{index + 1}. {score}",
                    self.small_font,
                    "white",
                    self.display_surface,
                    WINDOW_WIDTH // 2,
                    WINDOW_HEIGHT // 4 + 50 * (index + 1),
                )

            # Mostrar instrucción para regresar al menú
            self._draw_text(
                "Press ESC to return",
                self.small_font,
                "white",
                self.display_surface,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT - 50,
            )

            pygame.display.update()

            # Manejo de eventos para salir del menú de puntajes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Regresar al menú principal
                        show = False

    def _load_scores(self) -> List[int]:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as file:
                return json.load(file)
        return []


if __name__ == "__main__":
    game = Game()
    game.run()
