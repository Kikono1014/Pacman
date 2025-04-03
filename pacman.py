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