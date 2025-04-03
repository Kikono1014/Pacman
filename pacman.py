import pygame
from moveable import Moveable
from arena import Dot

class ClassName(object):
    def __init__(self, sprites, position, direction, speed, arena):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena
        self.next_direction = direction

    def update_destination(self):
        """ќбновл€ет направление, если возможно, и двигает Pac-Man."""
        if self.can_move(self.next_direction):
            self.direction = self.next_direction 
        
        if self.can_move(self.direction):
            super().update_destination()

    def can_move(self, direction):
        """ѕровер€ет, можно ли двигатьс€ в заданном направлении."""
        new_x = (self.position[0] + direction[0]) % len(self.arena.map[0])
        new_y = (self.position[1] + direction[1]) % len(self.arena.map)
        return self.arena.map[new_y][new_x] != Dot.WALL