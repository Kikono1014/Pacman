import pygame
from moveable import Moveable
from arena import Dot

class Pacman(Moveable):
    def __init__(self, sprites, position, direction, speed, arena):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena
        self.next_direction = direction

    def update_destination(self):
        if self.can_move(self.next_direction):
            self.direction = self.next_direction 
        
        if self.can_move(self.direction):
            super().update_destination()

    def can_move(self, direction):
        new_x = (self.position[0] + direction[0]) % len(self.arena.map[0])
        new_y = (self.position[1] + direction[1]) % len(self.arena.map)
        return self.arena.map[new_y][new_x] != Dot.WALL

    def rotate(self, direction):
        self.next_direction = direction

    def move(self, map):
        next_pos = ((self.position[0] + self.direction[0]) % len(map[0]), 
                    (self.position[1] + self.direction[1]) % len(map))

        if map[next_pos[1]][next_pos[0]] != Dot.WALL:
            self.position = next_pos
            self.arena.remove_dot(self.position)

    def set_direction(self, new_direction):
        next_pos = ((self.position[0] + new_direction[0]) % len(self.arena.map[0]),
                    (self.position[1] + new_direction[1]) % len(self.arena.map))

        if self.arena.map[next_pos[1]][next_pos[0]] != Dot.WALL:
            self.direction = new_direction