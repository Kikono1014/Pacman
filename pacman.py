import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot
from typing import Tuple

class PacMan(Moveable):
    def __init__(self, sprites: list[list[Sprite]], position: tuple[int, int], direction: tuple[int, int], speed: float, tile_size: int = 16):
        """Initialize Pac-Man with sprites, position, direction, speed, and tile size."""
        super().__init__(sprites[0], position, direction, speed)
        self.all_sprites = sprites
        self.lives: int = 3
        self.score: int = 0
        self.fruits: int = 0
        self.next_direction: Tuple[int, int] = direction
        self.animation_frame: float = 0.0
        self.animation_speed: float = 0.1
        self.game = None
        self.tile_size = tile_size

    def rotate(self, direction: tuple[int, int]):
        """Queue a new direction to be applied when possible."""
        self.next_direction = direction

    def can_move(self, direction: tuple[int, int]) -> bool:
        """Check if Pac-Man can move in the given direction from the current tile."""
        current_x, current_y = int(self.position[0]), int(self.position[1])
        next_x, next_y = current_x + direction[0], current_y + direction[1]
        if (0 <= next_y < len(self.game.arena.map) and 
            0 <= next_x < len(self.game.arena.map[0])):
            return self.game.arena.map[next_y][next_x] != Dot.WALL
        return False

    def update_position(self):
        """Update Pac-Man's position with strict grid-based movement and improved dot eating."""
        x, y = self.position
        at_tile_center = abs(x - int(x)) < 0.1 and abs(y - int(y)) < 0.1

        # Спробуємо з'їсти точку на поточній позиції незалежно від центру плитки
        current_x, current_y = int(x), int(y)
        if (0 <= current_y < len(self.game.arena.map) and 
            0 <= current_x < len(self.game.arena.map[0])):
            dot_type = self.game.arena.map[current_y][current_x]
            if dot_type in (Dot.NORMAL, Dot.PELLET, Dot.FRUIT):
                if dot_type == Dot.NORMAL:
                    self.score += 10
                elif dot_type == Dot.PELLET:
                    self.score += 50
                    for ghost in self.game.ghosts:
                        ghost.set_frightened()
                elif dot_type == Dot.FRUIT:
                    self.score += 100
                    self.fruits += 1
                self.game.arena.remove_dot((current_x, current_y))

        # Оновлюємо позицію
        if not at_tile_center:
            # Продовжуємо рухатися в поточному напрямку
            self.position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
        else:
            # Вирівнюємо до центру плитки
            self.position = (int(x + 0.5), int(y + 0.5))

            # Перевіряємо, чи можна змінити напрямок
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
            elif not self.can_move(self.direction):
                self.direction = (0, 0)

            # Рухаємося в новому напрямку, якщо можливо
            if self.direction != (0, 0) and self.can_move(self.direction):
                self.position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))

    def get_sprite(self) -> Sprite:
        """Return the current sprite based on direction and animation."""
        if self.direction != (0, 0):
            self.animation_frame = (self.animation_frame + self.animation_speed) % 3
        else:
            self.animation_frame = 0
        direction_map = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}
        direction_idx = direction_map.get(self.direction, 0)
        return self.all_sprites[direction_idx][int(self.animation_frame)]

    def get_hitbox(self) -> pygame.Rect:
        """Return the hitbox matching ghost logic."""
        sprite = self.get_sprite()
        return pygame.Rect(
            self.position[0] * sprite.area.w / 2,
            self.position[1] * sprite.area.h / 2,
            sprite.area.w,
            sprite.area.h
        )