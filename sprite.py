import pygame


class Sprite:
    def __init__(self, surface : pygame.Surface, area : pygame.Rect):
        self.texture : pygame.Surface = surface.subsurface(area)
        area.x = 0
        area.y = 0
        self.area : pygame.Rect = area

    def scale(self, scale):
        self.area.w *= scale;
        self.area.h *= scale;
        self.texture = pygame.transform.scale(self.texture, (self.area.w, self.area.h))