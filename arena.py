import pygame
from sprite import Sprite
from enum import Enum
from gameobject import GameObject
from random import choice

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

        with open(f'./data/arena{self.preset}/walls.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.map[y][x] = Dot.WALL
        
        with open(f'./data/arena{self.preset}/pellets.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.map[y][x] = Dot.PELLET
        
        with open(f'./data/arena{self.preset}/pacman_start.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.pacman_start = (x, y)
        
        with open(f'./data/arena{self.preset}/ghost_start.txt', 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                x = int(values[0])
                y = int(values[1])
                self.ghost_start = (x, y)
        

        
        for x in range(width):
            for y in range(height):
                if self.map[y][x] != Dot.WALL:
                    sprite = self.dot_sprites[2] if self.map[y][x] == Dot.PELLET else self.dot_sprites[0]
                    self.background.texture.blit(sprite.texture, self.get_dot_hitbox((x, y)), sprite.area)

    def remove_dot(self, position : tuple[int, int]):
        area = self.dot_sprites[1].area
        surface = pygame.surface.Surface((area.w/2, area.h/2))
        surface.fill((0, 0, 0))
        hitbox = self.get_dot_hitbox(position)
        hitbox.move_ip(area.w/4, area.h/4)
        self.background.texture.blit(surface, hitbox)


    def get_random_empty_dot(self) -> tuple[int, int]:
        empty = filter(lambda d: d == Dot.EMPTY, [dot for row in self.map for dot in row])

        # for x in range(len(self.map[0])):
        #     for y in range(len(self.map)):
        #         if self.map[y][x] == Dot.EMPTY:
        #             empty.append((x, y))

        return choice(empty)


    def get_dot_hitbox(self, position : tuple[int, int]):
        return pygame.Rect(
        position[0] * self.dot_sprites[1].area.w / 2,
        position[1] * self.dot_sprites[1].area.h / 2,
        self.dot_sprites[1].area.w,
        self.dot_sprites[1].area.h)

