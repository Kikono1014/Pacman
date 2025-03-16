import pygame


class Sprite:
    def __init__(self, surface : pygame.Surface, rect : pygame.Rect):
        self.texture : pygame.Surface = surface.subsurface(rect)
        self.area : pygame.Rect = rect