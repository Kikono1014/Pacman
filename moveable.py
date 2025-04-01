import pygame
from gameobject import GameObject
from sprite import Sprite
from arena import Dot

class Moveable(GameObject):
    def __init__(self, 
                 sprites: list[Sprite], 
                 position: tuple[float, float], 
                 direction: tuple[int, int],
                 speed: float):
        super().__init__(sprites, position)
        self.direction: tuple[int, int] = direction
        self.speed: float = speed
        self.target_position: tuple[float, float] = position

    def can_move(self, direction: tuple[int, int], arena) -> bool:
        current_x, current_y = int(self.position[0]), int(self.position[1])
        next_x, next_y = current_x + direction[0], current_y + direction[1]
        if 0 <= next_y < len(arena.map) and 0 <= next_x < len(arena.map[0]):
            return arena.map[next_y][next_x] != Dot.WALL
        return False

    def move(self, arena=None):
        if arena and not self.can_move(self.direction, arena):
            self.target_position = (int(self.position[0]), int(self.position[1]))  # Вирівнюємо з сіткою
            return

        current_x, current_y = self.position
        target_x, target_y = self.target_position
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0.05:
            step_x = dx * min(self.speed / distance, 1.0)
            step_y = dy * min(self.speed / distance, 1.0)
            new_x, new_y = current_x + step_x, current_y + step_y
            # Перевіряємо, чи нова позиція не веде до стіни
            if arena:
                next_pos = (int(new_x + self.direction[0]), int(new_y + self.direction[1]))
                if 0 <= next_pos[1] < len(arena.map) and 0 <= next_pos[0] < len(arena.map[0]):
                    if arena.map[next_pos[1]][next_pos[0]] != Dot.WALL:
                        self.position = (new_x, new_y)
        else:
            self.position = (int(target_x), int(target_y))  # Вирівнюємо з сіткою
            next_target = (int(target_x + self.direction[0]), int(target_y + self.direction[1]))
            if arena and self.can_move(self.direction, arena):
                self.target_position = next_target

    def rotate(self, direction: tuple[int, int]):
        self.direction = direction
    
    def get_hitbox(self):
        return pygame.Rect(
            self.position[0] * self.get_sprite().area.w / 2,
            self.position[1] * self.get_sprite().area.h / 2,
            self.get_sprite().area.w,
            self.get_sprite().area.h)