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

    def move(self, value : int):
        self.position = tuple(map(sum, zip(self.position, self.direction)))
        
        print(self.position)
        
    def get_hitbox(self):
        return pygame.Rect(
            (self.position[0] + 1) * self.get_sprite().area.w / 2,
            (self.position[1] + 1) * self.get_sprite().area.w / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)
    
    def get_sprite(self):
        return self.sprites[self.current]

    def rotate(self, direction : tuple[int, int]):
        self.direction = direction

    def change_sprite(self, id : int):
        self.current = id

