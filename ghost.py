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
        self.game = pacman.game
        self.name = name
        self.mode = "scatter"
        self.scatter_points = {
            "Blinky": (len(self.arena.map[0]) - 1, 0),
            "Pinky": (0, 0),
            "Inky": (len(self.arena.map[0]) - 1, len(self.arena.map) - 1),
            "Clyde": (0, len(self.arena.map) - 1),
        }
        self.scatter_point = self.scatter_points[name]
        self.frightened_timer = 0

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        if 0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0]):
            return self.arena.map[y][x] != Dot.WALL
        return False

    def update_destination(self):
        if self.mode == "chase":
            if self.name == "Blinky":
                self.destination = self.pacman.position
            elif self.name == "Pinky":
                pacman_dir = self.pacman.direction
                self.destination = (
                    self.pacman.position[0] + pacman_dir[0] * 4,
                    self.pacman.position[1] + pacman_dir[1] * 4
                )
            elif self.name == "Inky":
                blinky = next(g for g in self.game.ghosts if g.name == "Blinky")
                pacman_dir = self.pacman.direction
                intermediate = (
                    self.pacman.position[0] + pacman_dir[0] * 2,
                    self.pacman.position[1] + pacman_dir[1] * 2
                )
                self.destination = (
                    intermediate[0] + (intermediate[0] - blinky.position[0]),
                    intermediate[1] + (intermediate[1] - blinky.position[1])
                )
            elif self.name == "Clyde":
                distance = ((self.position[0] - self.pacman.position[0]) ** 2 + (self.position[1] - self.pacman.position[1]) ** 2) ** 0.5
                if distance > 8:
                    self.destination = self.pacman.position
                else:
                    self.destination = self.scatter_point
        elif self.mode == "scatter":
            self.destination = self.scatter_point

    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 60
        self.change_sprite(1)

    def move(self):
        self.update_destination()
        if self.mode == "frightened":
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "scatter"
                self.change_sprite(0)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for direction in directions:
                if self.can_move(direction):
                    self.rotate(direction)
                    super().move()
                    break
        else:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            best_direction = self.direction
            min_distance = float("inf")

            for direction in directions:
                if self.can_move(direction):
                    next_pos = tuple(map(sum, zip(self.position, direction)))
                    distance = ((next_pos[0] - self.destination[0]) ** 2 + (next_pos[1] - self.destination[1]) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = direction

            self.rotate(best_direction)
            if self.can_move(self.direction):
                super().move()