import pygame
from sprite import Sprite
from enum import Enum
from gameobject import GameObject
from random import choice

class Dot(Enum):
    NORMAL = 0  # Звичайна точка
    EMPTY = 1   # Порожня клітинка
    PELLET = 2  # Силова пелета (впливає на привидів)
    FRUIT = 3   # Фрукт (дає більше очок)
    WALL = 4    # Стіна

class Arena:
    def __init__(self, area: pygame.Rect, scale: float, dot_sprites: list[Sprite], preset: int):
        self.background = Sprite(pygame.image.load(f'sprites/arena{preset}.png'), area).scale(scale)
        self.dot_sprites = dot_sprites
        self.pacman_start: tuple[int, int] = None
        self.ghost_start: tuple[int, int] = None
        self.preset = preset
        self.build()

    def build(self):
        with open(f'./data/arena{self.preset}/size.txt', 'r') as file:
            values = file.readline().split(" ")
            width = int(values[0])
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

        # Додаємо звичайні точки всюди, де немає стін чи пелет
        for y in range(height):
            for x in range(width):
                if self.map[y][x] == Dot.NORMAL:
                    self.objects[y][x].change_sprite(0)  # Спрайт для звичайної точки

        with open(f'./data/arena{self.preset}/pacman_start.txt', 'r') as file:
            values = file.readline().split(" ")
            x = int(values[0])
            y = int(values[1])
            self.pacman_start = (x, y)

        with open(f'./data/arena{self.preset}/ghost_start.txt', 'r') as file:
            values = file.readline().split(" ")
            x = int(values[0])
            y = int(values[1])
            self.ghost_start = (x, y)

    def remove_dot(self, position: tuple[int, int]):
        """Видаляє точку, пелету або фрукт з позиції"""
        x, y = position
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
            if self.map[y][x] in (Dot.NORMAL, Dot.PELLET, Dot.FRUIT):
                self.map[y][x] = Dot.EMPTY
                self.objects[y][x].change_sprite(1)  # Спрайт порожньої клітинки

    def get_dots(self, filter: Dot = Dot.NORMAL) -> list[tuple[int, int]]:
        """Повертає список координат точок певного типу"""
        return [
            (x, y)
            for y, row in enumerate(self.map)
            for x, dot in enumerate(row)
            if dot == filter
        ]

    def add_fruit(self, pacman_fruits: int):
        """Додає фрукт у випадкову порожню клітинку, вибираючи тип залежно від кількості з'їдених фруктів"""
        empty = self.get_dots(Dot.EMPTY)
        if not empty:
            return
        
        position = choice(empty)
        x, y = position
        
        # Визначаємо індекс фрукта на основі кількості з'їдених фруктів
        fruit_sprites = self.dot_sprites[3:]  # Усі спрайти фруктів (індекси 3 і далі)
        fruit_index = pacman_fruits % len(fruit_sprites) + 3  # Циклічно обираємо фрукт
        self.map[y][x] = Dot.FRUIT
        self.objects[y][x].change_sprite(fruit_index)  # Встановлюємо спрайт фрукта