from typing import Tuple

import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        surf: pygame.Surface,
        pos: Tuple[float, float],
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.image = surf
        self.rect: pygame.FRect = self.image.get_frect(midbottom=pos)

    def update(self, dt, *groups) -> None:
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
