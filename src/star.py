from random import randint

import pygame

from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf: pygame.Surface):
        super().__init__(groups)
        self.image = surf
        self.rect: pygame.FRect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )
