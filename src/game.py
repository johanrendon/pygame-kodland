from pathlib import Path
from random import randint
from typing import List

import pygame
from pygame.display import message_box
from pygame.sprite import collide_mask

from meteor import Meteor
from player import Player
from settings import WINDOW_HEIGHT, WINDOW_WIDTH
from star import Star


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space shooter")
        self.running = True
        self.clock = pygame.time.Clock()

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

    def run(self):
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
            self.display_surface.fill("#3a2e3f")
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

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
                laser.kill()


if __name__ == "__main__":
    game = Game()
    game.run()
