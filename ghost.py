import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot
import random

class Ghost(Moveable):
    def __init__(self, sprites: list[list[Sprite]], position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman):
        super().__init__(sprites[0], position, direction, speed)
        self.destination: tuple[int, int] = position
        self.arena = arena
        self.pacman = pacman
        self.game = pacman.game
        self.mode = "scatter"
        self.frightened_timer = 0
        self.base_speed = speed
        self.respawn_timer = 0
        self.is_active = True
        self.mode_schedule = [
            (420, "scatter"),  # 7 seconds
            (1200, "chase"),   # 20 seconds
            (420, "scatter"),  # 7 seconds
            (1200, "chase"),   # 20 seconds
            (300, "scatter"),  # 5 seconds
            (1200, "chase"),   # 20 seconds
            (300, "scatter"),  # 5 seconds
            (-1, "chase")      # Infinite chase
        ]
        self.mode_index = 0
        self.mode_timer = 0
        self.sprites = sprites
        self.current_frame = 0
        self.animation_speed = 0.05  # Зменшено для плавнішої анімації (12 кадрів при 60 FPS)

    def get_sprite(self):
        self.current_frame = (self.current_frame + self.animation_speed) % 2
        if self.mode == "frightened":
            # Лише два перших спрайти (сині) до останніх 2 секунд, потім миготіння з білими
            if self.frightened_timer > 120:  # Перші 5 секунд (420 - 120 = 300 кадрів)
                return self.sprites[4][int(self.current_frame)]  # Лише сині (0 і 1)
            else:  # Останні 2 секунди
                return self.sprites[4][int(self.current_frame * 2) % 4]  # Миготіння (0, 1, 2, 3)
        else:
            direction_id = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}.get(self.direction, 0)
            return self.sprites[direction_id][int(self.current_frame)]

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        # Wrap coordinates for collision check
        x = x % len(self.arena.map[0])
        y = y % len(self.arena.map)
        return self.arena.map[y][x] != Dot.WALL

    def check_collision(self, pacman):
        pacman_hitbox = pacman.get_hitbox()
        ghost_hitbox = self.get_hitbox()
        return pacman_hitbox.colliderect(ghost_hitbox)

    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 420  # 7 seconds at 60 FPS
        self.current_frame = 0

    def update_destination(self):
        pass  # Overridden in subclasses

    def move(self, arena_map: list[list[Dot]]):
        if not self.is_active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_active = True
                self.position = self.arena.ghost_start
                self.mode_index = 0
                self.mode_timer = 0
            return

        # Update mode based on schedule
        current_duration, current_mode = self.mode_schedule[self.mode_index]
        self.mode_timer += 1
        if current_duration != -1 and self.mode_timer >= current_duration:
            self.mode_timer = 0
            self.mode_index = min(self.mode_index + 1, len(self.mode_schedule) - 1)
            self.mode = self.mode_schedule[self.mode_index][1]

        if self.mode != "frightened":
            self.update_destination()

        # Move only at intersections
        if self.position[0] % 1 < 0.1 and self.position[1] % 1 < 0.1:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_directions = [d for d in directions if self.can_move(d) and d != tuple(-x for x in self.direction)]
            if not valid_directions:
                valid_directions = [d for d in directions if self.can_move(d)]

            if valid_directions:
                if self.mode == "frightened":
                    self.speed = self.base_speed * 0.5
                    self.frightened_timer -= 1
                    if self.frightened_timer <= 0:
                        self.mode = self.mode_schedule[self.mode_index][1]
                    best_direction = max(
                        valid_directions,
                        key=lambda d: ((self.position[0] + d[0] - self.pacman.position[0]) ** 2 +
                                       (self.position[1] + d[1] - self.pacman.position[1]) ** 2) ** 0.5
                    )
                    self.rotate(best_direction)
                else:
                    self.speed = self.base_speed
                    best_direction = min(
                        valid_directions,
                        key=lambda d: ((self.position[0] + d[0] - self.destination[0]) ** 2 +
                                       (self.position[1] + d[1] - self.destination[1]) ** 2) ** 0.5
                    )
                    self.rotate(best_direction)

        # Use Moveable's move method to handle position update with wrapping
        super().move()