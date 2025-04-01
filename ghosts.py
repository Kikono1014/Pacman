import pygame
from ghost import Ghost
from sprite import Sprite

class Blinky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        row = 4 * 16
        sprites = [
            # right
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            # left
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            # up
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            # down
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            # Scared
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
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
        row = 5 * 16
        sprites = [
            # right
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            # left
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            # up
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            # down
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            # Scared
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
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
        row = 6 * 16
        sprites = [
            # right
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            # left
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            # up
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            # down
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            # Scared
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
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
        row = 7 * 16
        sprites = [
            # right
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            # left
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            # up
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            # down
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            # Scared
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
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