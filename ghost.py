import pygame
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

    def update_destination(self):
        pass