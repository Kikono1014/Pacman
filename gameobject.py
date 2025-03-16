import pygame
from sprite import Sprite

class GameObject:
    def __init__(self,
                 sprites : list[Sprite], 
                 position : tuple[int, int], 
                 direction : tuple[int, int],
                 speed : float
                 ):
        self.sprites : list[Sprite] = sprites
        self.current : int = 0
        self.position : tuple[int, int] = position
        self.direction : tuple[int, int] = direction
        self.speed : float = speed

    def move(self):
        self.position = tuple(map(sum, zip(self.position, self.direction)))
        
    def get_hitbox(self):
        return pygame.Rect(
            (self.position[0] + 1) * self.speed * self.get_sprite().area.w / 16,
            (self.position[1] + 1) * self.speed * self.get_sprite().area.w / 16,
            self.get_sprite().area.w,
            self.get_sprite().area.h)
    
    def get_sprite(self):
        return self.sprites[self.current]

    def rotate(self, direction : tuple[int, int]):
        self.direction = direction

    def change_sprite(self, id : int):
        self.current = id

