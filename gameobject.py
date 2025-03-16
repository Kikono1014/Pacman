import pygame
from sprite import Sprite

class GameObject:
    def __init__(self,
                 sprites : list[Sprite], 
                 position : tuple[int, int], 
                 direction : tuple[int, int],
                 hitbox : pygame.Rect):
        self.sprites : list[Sprite] = sprites
        self.current : int = 0
        self.position : tuple[int, int] = position
        self.direction : tuple[int, int] = direction
        self.hitbox : pygame.Rect = hitbox

    def move(self, value : int):
        pass

    def rotate(self, direction : tuple[int, int]):
        self.direction = direction

    def change_sprite(self, id : int):
        self.current = id

