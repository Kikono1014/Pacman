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
        self.mode_timer = 0
        self.mode_duration = 420  # 7 секунд при 60 FPS

        self.sprites = sprites
        self.current_frame = 0
        self.animation_speed = 0.1

    def get_sprite(self):
        self.current_frame = (self.current_frame + self.animation_speed) % 2
        if self.mode == "frightened":
            return self.sprites[4][int(self.current_frame) % 2]  # Анімація наляканого стану
        else:
            direction_id = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}.get(self.direction, 0)
            return self.sprites[direction_id][int(self.current_frame)]

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        if 0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0]):
            if self.arena.map[y][x] == Dot.WALL:
                return False
            for other_ghost in self.game.ghosts:
                if other_ghost != self and other_ghost.is_active:
                    other_x, other_y = int(other_ghost.position[0]), int(other_ghost.position[1])
                    if other_x == x and other_y == y:
                        return False
            return True
        return False

    def check_collision(self, pacman):
        pacman_hitbox = pacman.get_hitbox()
        ghost_hitbox = self.get_hitbox()
        return pacman_hitbox.colliderect(ghost_hitbox)

    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 420  # 7 секунд при 60 FPS
        self.current_frame = 0

    def update_destination(self):
        # Цей метод буде перевизначений у дочірніх класах
        pass

    def move(self):
        if not self.is_active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_active = True
                self.mode = "scatter"
            return

        # Оновлення режимів
        if self.mode != "frightened":
            self.mode_timer += 1
            if self.mode_timer >= self.mode_duration:
                self.mode_timer = 0
                self.mode = "chase" if self.mode == "scatter" else "scatter"

        self.update_destination()

        # Рух лише на перехрестях
        if self.position[0] % 1 < 0.1 and self.position[1] % 1 < 0.1:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_directions = [d for d in directions if self.can_move(d) and d != tuple(-x for x in self.direction)]  # Без повороту назад
            if not valid_directions:  # Якщо немає варіантів, крім повороту назад
                valid_directions = [d for d in directions if self.can_move(d)]

            if self.mode == "frightened":
                self.speed = self.base_speed * 0.5
                self.frightened_timer -= 1
                if self.frightened_timer <= 0:
                    self.mode = "scatter"
                if valid_directions:
                    self.rotate(valid_directions[random.randint(0, len(valid_directions) - 1)])
            else:
                self.speed = self.base_speed
                if valid_directions:
                    best_direction = min(
                        valid_directions,
                        key=lambda d: ((self.position[0] + d[0] - self.destination[0]) ** 2 +
                                       (self.position[1] + d[1] - self.destination[1]) ** 2) ** 0.5
                    )
                    self.rotate(best_direction)

        # Плавний рух
        next_pos = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
        self.position = next_pos

        # Перевірка колізії з PacMan
        if self.check_collision(self.pacman):
            if self.mode == "frightened":
                self.position = self.arena.ghost_start
                self.is_active = False
                self.respawn_timer = 120
                # Очки не додаємо, бо це логіка PacMan
            else:
                self.pacman.position = self.arena.pacman_start
                # Штраф не віднімаємо, бо це логіка PacMan