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
        self.next_position: Tuple[int, int] = position  # Intended next position
        self.animation_frame = 0
        self.animation_speed = 0.1

    def update_position(self):
        """Updates Pac-Man's position based on direction and checks for valid movement."""
        # Calculate the next intended position
        self.next_position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
        
        # Check if the next position is valid (not a wall)
        next_x, next_y = int(self.next_position[0]), int(self.next_position[1])
        if (0 <= next_y < len(self.game.arena.map) and 
            0 <= next_x < len(self.game.arena.map[0]) and 
            self.game.arena.map[next_y][next_x] != Dot.WALL):
            self.position = self.next_position
        
        # Handle pellet/fruit consumption
        current_x, current_y = int(self.position[0]), int(self.position[1])
        if self.game.arena.map[current_y][current_x] == Dot.PELLET:
            self.game.arena.map[current_y][current_x] = Dot.EMPTY
            self.game.arena.objects[current_y][current_x].change_sprite(0)
            self.score += 10
            for ghost in self.game.ghosts:
                ghost.set_frightened()
        elif self.game.arena.map[current_y][current_x] == Dot.FRUIT:
            self.game.arena.map[current_y][current_x] = Dot.EMPTY
            self.game.arena.objects[current_y][current_x].change_sprite(0)
            self.score += 100  # Example fruit score
            self.fruits += 1

    def get_sprite(self):
        """Returns the current sprite with animation."""
        self.animation_frame = (self.animation_frame + self.animation_speed) % 3
        return self.sprites[int(self.animation_frame)]