import pygame
import random
from moveable import Moveable
from sprite import Sprite
from arena import Dot

class Ghost(Moveable):
    def __init__(self, sprites: list[Sprite], position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, name: str):
        super().__init__(sprites, position, direction, speed)
        self.destination: tuple[int, int] = position
        self.arena = arena
        self.pacman = pacman
        self.name = name
        self.mode = "scatter"
        self.scatter_points = {
            "Blinky": (len(self.arena.map[0]) - 1, 0),
            "Pinky": (0, 0),
            "Inky": (len(self.arena.map[0]) - 1, len(self.arena.map) - 1),
            "Clyde": (0, len(self.arena.map) - 1),
        }
        self.scatter_point = self.scatter_points[name]

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        if 0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0]):
            return self.arena.map[y][x] != Dot.WALL
        return False

    def update_destination(self):
        pass

    def move(self):
        if self.can_move(self.direction):
            super().move()
        else:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for direction in directions:
                if self.can_move(direction):
                    self.rotate(direction)
                    super().move()
                    break