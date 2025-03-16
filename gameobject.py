import pygame
from sprite import Sprite

class GameObject:
    def __init__(self,
                 sprites : list[Sprite], 
                 position : tuple[int, int], 
                 direction : tuple[int, int]):
        self.sprites : list[Sprite] = sprites
        self.current : int = 0
        self.position : tuple[int, int] = position
        self.direction : tuple[int, int] = direction

    def move(self, value : int):
        pass

    def rotate(self, direction : tuple[int, int]):
        pass

    def change_sprite(self, id : int):
        pass

