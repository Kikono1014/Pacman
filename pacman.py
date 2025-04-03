import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot
from typing import Tuple

class PacMan(Moveable):
    def __init__(self, sprites: list[Sprite], position: tuple[int, int], direction: tuple[int, int], speed: float):
        super().__init__(sprites, position, direction, speed)
        self.lives: int = 3
        self.score: int = 0
        self.fruits: int = 0
        self.animation_frame = 0
        self.animation_speed = 0.1

    def update_destination(self, arena_map : list[list[Dot]]):
        """Updates Pac-Man's position based on direction and checks for valid movement."""
        # Calculate the next intended position
        super().update_destination(arena_map)
        
        # Check if the next position is valid (not a wall)
        next_x, next_y = int(self.destination[0]), int(self.destination[1])
        if (arena_map[next_y][next_x] == Dot.WALL):
            self.destination = self.position
    
    def move(self):
        super().move()
        

    def get_sprite(self):
        """Returns the current sprite with animation."""
        self.animation_frame = (self.animation_frame + self.animation_speed) % 3
        return self.sprites[int(self.animation_frame)]