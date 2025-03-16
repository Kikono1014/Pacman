import pygame


class Sprite:
    def __init__(self, surface : pygame.Surface, rect : pygame.Rect):
        self.texture = surface
        self.area = rect