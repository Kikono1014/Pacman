import pygame
from sprite import Sprite
from enum import Enum
from gameobject import GameObject


class Dot(Enum):
    NORMAL = 0
    EMPTY= 1
    PELLET = 2
    FRUIT = 3
    WALL = 4

class Arena:
    def __init__(self,
                 area : pygame.Rect,
                 scale : float,
                 dot_sprites : list[Sprite],
                 preset : int):
        self.background = Sprite(pygame.image.load(f'sprites/arena{preset}.png'), area).scale(scale)
        self.dot_sprites = dot_sprites
        self.pacman_start : tuple[int, int] = None
        self.ghost_start  : tuple[int, int] = None
        self.preset = preset

        self.build()

    def build(self):
        with open(f'./data/arena{self.preset}/size.txt', 'r') as file:
            values = file.readline().split(" ")
            width  = int(values[0])
            height = int(values[1])
            self.map = [[Dot.NORMAL for _ in range(width)] for _ in range(height)]
            self.objects = [[GameObject(self.dot_sprites, (x, y)) for x in range(width)] for y in range(height)]

        with open(f'./data/arena{self.preset}/walls.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.map[y][x] = Dot.WALL
                self.objects[y][x].change_sprite(1)
        
        with open(f'./data/arena{self.preset}/pellets.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.map[y][x] = Dot.PELLET
                self.objects[y][x].change_sprite(2)
