import pygame
from gameobject import GameObject
from sprite import Sprite
from arena import Dot

class Moveable(GameObject):
    def __init__(self, sprites, position, direction, speed):
        super().__init__(sprites, position)
        self.direction = direction
        self.speed = speed
        self.buffered_direction = None
        """Creates moveable game object

         - sprites: list of Sprite objects that can be used in this object
         - position: position on the map in dot coordinates
         - direction: direction of movement right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1]
         - speed: speed of movement, pixels per frame
        """
        super().__init__(sprites, position)
        self.direction : tuple[int, int] = direction
        self.speed : float = speed


    
    def move(self, arena):
        next_position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

        if arena.map[next_position[1]][next_position[0]] != Dot.WALL:
            self.position = next_position
        else:
            if self.buffered_direction:
                buffered_next = (self.position[0] + self.buffered_direction[0], self.position[1] + self.buffered_direction[1])
                if arena.map[buffered_next[1]][buffered_next[0]] != Dot.WALL:
                    self.direction = self.buffered_direction  # Меняем направление
                    self.position = buffered_next  
                self.buffered_direction = None

    # Проверяем, съел ли Пакман монетку на новой позиции
        if arena.map[self.position[1]][self.position[0]] in [Dot.NORMAL, Dot.PELLET]:
            arena.map[self.position[1]][self.position[0]] = Dot.EMPTY
            arena.objects[self.position[1]][self.position[0]].change_sprite(1)

    def rotate(self, new_direction, arena):
        next_position = (self.position[0] + new_direction[0], self.position[1] + new_direction[1])
        if next_position and next_position[1] >= 0 and next_position[0] >= 0:  
           if arena.map[next_position[1]][next_position[0]] != Dot.WALL:
               self.direction = new_direction  # Поворачиваем сразу
               self.buffered_direction = None  # Сбрасываем буфер
           else:
               self.buffered_direction = new_direction

    
    def get_hitbox(self):
        # self.get_sprite().area.w / 2 is a size of a cell
        return pygame.Rect(
            self.position[0] * self.get_sprite().area.w / 2,
            self.position[1] * self.get_sprite().area.h / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)