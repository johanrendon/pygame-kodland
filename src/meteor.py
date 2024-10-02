from random import randint, uniform
from typing import Tuple

import pygame


class Meteor(pygame.sprite.Sprite):
    def __init__(
        self,
        surf: pygame.Surface,
        pos: Tuple[float, float],
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.original_surf = surf
        self.image = surf
        self.rect: pygame.FRect = self.image.get_frect(center=pos)
        self.start_time: int = pygame.time.get_ticks()
        self.lifetime: int = 3000
        self.direction: pygame.Vector2 = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed: int = randint(400, 500)
        self.rotation_speed: int = randint(40, 80)
        self.rotation: float = 0

    def update(self, dt, *groups) -> None:
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
