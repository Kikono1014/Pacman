import pygame

class Sprite:
    def __init__(self, surface: pygame.Surface, area: pygame.Rect):
        """Creates a sprite
         - surface: pygame surface to crop sprite from
         - area: pygame rect, area of sprite on the surface
        """
        self.texture: pygame.Surface = surface.subsurface(area)
        area.x = 0
        area.y = 0
        self.area: pygame.Rect = area

    def scale(self, scale):
        self.area.w *= scale
        self.area.h *= scale
        self.texture = pygame.transform.scale(self.texture, (self.area.w, self.area.h))
        return self