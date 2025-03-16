import pygame


class Sprite:
    def __init__(self, surface : pygame.Surface, rect : pygame.Rect):
        self.texture : pygame.Surface = surface
        self.area : pygame.Rect = rect