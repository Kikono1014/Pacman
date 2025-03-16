import pygame
from gameobject import GameObject
from sprite import Sprite

class Moveable(GameObject):
    def __init__(self, 
                 sprites : list[Sprite], 
                 position : tuple[int, int], 
                 direction : tuple[int, int],
                 speed : float):
        """Creates moveable game object

         - sprites: list of Sprite objects that can be used in this object
         - position: position on the map in dot coordinates
         - direction: direction of movement right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1]
         - speed: speed of movement, pixels per frame
        """
        super().__init__(sprites, position)
        self.direction : tuple[int, int] = direction
        self.speed : float = speed


    
    def move(self):
        self.position = tuple(map(sum, zip(self.position, self.direction)))

    def rotate(self, direction : tuple[int, int]):
        self.direction = direction

    
    def get_hitbox(self):
        # self.get_sprite().area.w / 2 is offset
        return pygame.Rect(
            (self.position[0] + 1) * self.get_sprite().area.w / 2,
            (self.position[1] + 1) * self.get_sprite().area.h / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)