from ghost import Ghost
from sprite import Sprite
import pygame

class Blinky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        sprites = [
            Sprite(atlas, pygame.Rect(0, 4 * 16, 16, 16)).scale(scale),
            Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (len(self.arena.map[0]) - 1, 0)

    def update_destination(self):
        if self.mode == "chase":
            self.destination = self.pacman.position
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Pinky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        sprites = [
            Sprite(atlas, pygame.Rect(0, 5 * 16, 16, 16)).scale(scale),
            Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (0, 0)

    def update_destination(self):
        if self.mode == "chase":
            pacman_dir = self.pacman.direction
            self.destination = (
                self.pacman.position[0] + pacman_dir[0] * 4,
                self.pacman.position[1] + pacman_dir[1] * 4
            )
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Inky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        sprites = [
            Sprite(atlas, pygame.Rect(0, 6 * 16, 16, 16)).scale(scale),
            Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (len(self.arena.map[0]) - 1, len(self.arena.map) - 1)

    def update_destination(self):
        if self.mode == "chase":
            blinky = next(g for g in self.game.ghosts if isinstance(g, Blinky))
            pacman_dir = self.pacman.direction
            intermediate = (
                self.pacman.position[0] + pacman_dir[0] * 2,
                self.pacman.position[1] + pacman_dir[1] * 2
            )
            self.destination = (
                intermediate[0] + (intermediate[0] - blinky.position[0]),
                intermediate[1] + (intermediate[1] - blinky.position[1])
            )
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Clyde(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        sprites = [
            Sprite(atlas, pygame.Rect(0, 7 * 16, 16, 16)).scale(scale),
            Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (0, len(self.arena.map) - 1)

    def update_destination(self):
        if self.mode == "chase":
            distance = ((self.position[0] - self.pacman.position[0]) ** 2 + 
                        (self.position[1] - self.pacman.position[1]) ** 2) ** 0.5
            if distance > 8:
                self.destination = self.pacman.position
            else:
                self.destination = self.scatter_point
        elif self.mode == "scatter":
            self.destination = self.scatter_point