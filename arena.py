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

        if (self.map[position[1]][position[0]] == Dot.EMPTY):
            return

        if (self.map[position[1]][position[0]] != Dot.FRUIT):
            surface = pygame.surface.Surface((area.w/2, area.h/2))
            surface.fill((0, 0, 0))
            hitbox = self.get_dot_hitbox(position)
            hitbox.move_ip(area.w/4, area.h/4)
            self.background.texture.blit(surface, hitbox)
        else:
            surface = pygame.surface.Surface((area.w - area.w / 8, area.h - area.h / 8))
            surface.fill((0, 0, 0))
            hitbox = self.get_dot_hitbox(position)
            hitbox.move_ip(area.w/16, area.h/16)
            self.background.texture.blit(surface, hitbox)

        self.map[position[1]][position[0]] = Dot.EMPTY


    def get_dots(self, filter: Dot = Dot.NORMAL) -> tuple[int, int]:
        return [
            (x, y)
            for y, row in enumerate(self.map)
            for x, dot in enumerate(row)
            if dot == filter
        ]

    def add_fruit(self):
        empty = self.get_dots(Dot.EMPTY)
        if (len(empty) == 0): 
            return
        
        position = choice(empty)

        sprite = choice(self.dot_sprites[3:])
        
        hitbox = self.get_dot_hitbox(position)

        self.background.texture.blit(sprite.texture, hitbox, sprite.area)

        self.map[position[1]][position[0]] = Dot.FRUIT
                
            
        

    def get_dot_hitbox(self, position : tuple[int, int]):
        return pygame.Rect(
        position[0] * self.dot_sprites[1].area.w / 2,
        position[1] * self.dot_sprites[1].area.h / 2,
        self.dot_sprites[1].area.w,
        self.dot_sprites[1].area.h)

