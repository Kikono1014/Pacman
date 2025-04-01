import pygame
from sprite import Sprite

class GameObject:
    def __init__(self, sprites: list[Sprite], position: tuple[int, int]):
        """Creates game object
         - sprites: list of Sprite objects that can be used in this object
         - position: position on the map in dot coordinates
        """
        self.sprites: list[Sprite] = sprites
        self.current: int = 0
        self.position: tuple[int, int] = position

    def get_hitbox(self):
        """Returns area where to draw object"""
        return pygame.Rect(
            self.position[0] * self.get_sprite().area.w / 2,
            self.position[1] * self.get_sprite().area.h / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)

    def get_sprite(self):
        return self.sprites[self.current]

    def change_sprite(self, id: int):
        self.current = id

