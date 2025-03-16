import pygame
from sprite import Sprite
from enum import Enum


class Dot(Enum):
    NORMAL = 0
    EMPTY= 1
    PELLET = 2
    FRUIT = 3
    WALL = 4
    GATE = 5

class Arena:
    def __init__(self, 
                 background : Sprite,
                 dot_sprites : list[Sprite],
                 preset : int):
        self.background = background
        self.dot_sprites = dot_sprites
        self.pacman_start : tuple[int, int] = None
        self.ghost_start  : tuple[int, int] = None

        self.build(preset)

    def build(self, preset):
        with open(f'./data/arena{preset}/.txt', 'r') as file:
            values = file.readline().split(" ")
            width  = int(values[0])
            height = int(values[1])
            self.map = [[[Dot.NORMAL] for _ in range(width)] for _ in range(height)]

        with open(f'./data/arena{preset}/walls.txt', 'r') as file:
            values = file.readline().split(" ")
            x = int(values[0])
            y = int(values[1])
            map[y][x] = Dot.WALL
        
        with open(f'./data/arena{preset}/bonuses.txt', 'r') as file:
            values = file.readline().split(" ")
            x = int(values[0])
            y = int(values[1])
            map[y][x] = Dot.Bonus
        
        with open(f'./data/arena{preset}/gate.txt', 'r') as file:
            values = file.readline().split(" ")
            x = int(values[0])
            y = int(values[1])
            map[y][x] = Dot.GATE