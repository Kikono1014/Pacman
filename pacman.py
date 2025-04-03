import pygame
from moveable import Moveable
from arena import Dot

class ClassName(object):
    def __init__(self, sprites, position, direction, speed, arena):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena
        self.next_direction = direction

