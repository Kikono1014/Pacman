import pygame
from gameobject import GameObject
from sprite import Sprite
from arena import Dot

class Moveable(GameObject):
    def __init__(self, sprites: list[Sprite], position: tuple[int, int], direction: tuple[int, int], speed: float):
        """Creates moveable game object
         - sprites: list of Sprite objects that can be used in this object
         - position: position on the map in dot coordinates
         - direction: direction of movement right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1]
         - speed: speed of movement, pixels per frame
        """
        super().__init__(sprites, position)
        self.direction: tuple[int, int] = direction
        self.speed: float = speed
        # Reference to arena will be set by subclasses
        self.arena = None

    def move(self):
        # Smooth movement: update position based on direction and speed
        new_position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
        
        # Get map dimensions and wrap around
        if self.arena:
            map_width = len(self.arena.map[0])
            map_height = len(self.arena.map)
            
            x, y = new_position
            if x < 0:
                x += map_width
            elif x >= map_width:
                x -= map_width
            if y < 0:
                y += map_height
            elif y >= map_height:
                y -= map_height
                
            self.position = (x, y)
        else:
            # Fallback if arena is not set
            self.position = new_position

    def rotate(self, direction: tuple[int, int]):
        self.direction = direction
    
    def get_hitbox(self):
        return pygame.Rect(
            self.position[0] * self.get_sprite().area.w / 2,
            self.position[1] * self.get_sprite().area.h / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)