import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot
import random
import heapq
import time

class Ghost(Moveable):
    def __init__(self, sprites: list[list[Sprite]], position: tuple[float, float], direction: tuple[int, int], speed: float, arena, pacman):
        super().__init__(sprites[0], position, direction, speed)
        self.destination: tuple[int, int] = (int(position[0]), int(position[1]))
        self.arena = arena
        self.pacman = pacman
        self.game = pacman.game
        self.mode = "scatter"
        self.frightened_timer = 0
        self.base_speed = speed
        self.respawn_timer = 0
        self.is_active = True
        self.mode_timer = 0
        self.mode_duration = 600
        self.sprites = sprites
        self.path = []
        self.last_path_update = 0
        self.path_update_interval = 0.5

    def get_sprite(self):
        if self.mode == "frightened":
            self.current = (self.current + 1) % 4
            return self.sprites[4][self.current]
        else:
            directionID = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}
            dir_id = directionID.get(self.direction, 0)
            self.current = (self.current + 1) % 2
            return self.sprites[dir_id][self.current]

    def can_move(self, direction: tuple[int, int], arena=None) -> bool:
        # Спочатку перевіряємо стіни через базовий клас
        if not super().can_move(direction, self.arena):
            return False
        
        # Додаткова перевірка на зіткнення з іншими привидами
        next_pos = (int(self.position[0] + direction[0]), int(self.position[1] + direction[1]))
        x, y = next_pos
        if 0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0]):
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
        self.frightened_timer = 420
        self.path = []

    def heuristic(self, pos: tuple[int, int], target: tuple[int, int]) -> float:
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    def find_path(self, start: tuple[int, int], target: tuple[int, int], max_nodes=1000) -> list[tuple[int, int]]:
        start = (int(start[0]), int(start[1]))
        target = (int(target[0]), int(target[1]))
        if not (0 <= target[1] < len(self.arena.map) and 0 <= target[0] < len(self.arena.map[0])):
            return []
        if self.arena.map[target[1]][target[0]] == Dot.WALL:
            return []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        frontier = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}
        nodes_processed = 0

        while frontier and nodes_processed < max_nodes:
            current = heapq.heappop(frontier)[1]
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            nodes_processed += 1
            for direction in directions:
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                if not self.can_move(direction):  # Використовуємо self.arena
                    continue
                tentative_g_score = g_score[current] + 1
                if next_pos not in g_score or tentative_g_score < g_score[next_pos]:
                    came_from[next_pos] = current
                    g_score[next_pos] = tentative_g_score
                    f_score[next_pos] = tentative_g_score + self.heuristic(next_pos, target)
                    heapq.heappush(frontier, (f_score[next_pos], next_pos))
        return []

    def get_random_accessible_point(self) -> tuple[int, int]:
        for _ in range(10):
            x = random.randint(0, len(self.arena.map[0]) - 1)
            y = random.randint(0, len(self.arena.map) - 1)
            if self.arena.map[y][x] != Dot.WALL:
                return (x, y)
        return self.arena.ghost_start

    def move(self):
        if not self.is_active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_active = True
                self.position = self.arena.ghost_start
                self.target_position = self.position
                self.mode = "scatter"
                self.path = []
            return

        current_time = time.time()
        current_pos = (int(self.position[0]), int(self.position[1]))

        # Оновлення режимів
        if self.mode != "frightened":
            self.mode_timer += 1
            if self.mode_timer >= self.mode_duration:
                self.mode_timer = 0
                self.mode = "chase" if self.mode == "scatter" else "scatter"
                self.path = []
        elif self.mode == "frightened":
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "scatter"
                self.path = []

        # Оновлення шляху
        self.update_destination()
        if (not self.path or self.path[-1] != self.destination) and self.mode != "frightened":
            if current_time - self.last_path_update >= self.path_update_interval:
                self.path = self.find_path(current_pos, self.destination)
                self.last_path_update = current_time
                if not self.path:
                    self.destination = self.get_random_accessible_point()
                    self.path = self.find_path(current_pos, self.destination)

        # Рух по шляху
        if self.mode == "frightened":
            self.speed = self.base_speed * 0.5
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for direction in directions:
                if self.can_move(direction):
                    self.rotate(direction)
                    break
            super().move(self.arena)
            self.path = []
        else:
            self.speed = self.base_speed
            if self.path and abs(self.position[0] - self.target_position[0]) < 0.05 and abs(self.position[1] - self.target_position[1]) < 0.05:
                next_pos = self.path[0]
                direction = (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
                if self.can_move(direction):
                    self.rotate(direction)
                    self.target_position = (next_pos[0], next_pos[1])
                    self.path.pop(0)
            elif not self.path:
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for direction in directions:
                    if self.can_move(direction):
                        self.rotate(direction)
                        break
            super().move(self.arena)

        # Колізія з PacMan
        if self.check_collision(self.pacman):
            if self.mode == "frightened":
                self.position = self.arena.ghost_start
                self.target_position = self.position
                self.is_active = False
                self.respawn_timer = 120
                self.path = []
            else:
                self.pacman.position = self.arena.pacman_start
                self.pacman.target_position = self.pacman.position

    def update_destination(self):
        pass  # Перевизначається у дочірніх класах


class Blinky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        row = 4 * 16
        sprites = [
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (len(self.arena.map[0]) - 1, 0)

    def update_destination(self):
        if self.mode == "chase":
            self.destination = (int(self.pacman.position[0]), int(self.pacman.position[1]))
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Pinky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        row = 5 * 16
        sprites = [
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (0, 0)

    def update_destination(self):
        if self.mode == "chase":
            pacman_dir = self.pacman.direction
            self.destination = (
                int(self.pacman.position[0] + pacman_dir[0] * 4),
                int(self.pacman.position[1] + pacman_dir[1] * 4)
            )
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Inky(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        row = 6 * 16
        sprites = [
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (len(self.arena.map[0]) - 1, len(self.arena.map) - 1)

    def update_destination(self):
        if self.mode == "chase":
            blinky = next(g for g in self.game.ghosts if isinstance(g, Blinky))
            pacman_dir = self.pacman.direction
            intermediate = (
                int(self.pacman.position[0] + pacman_dir[0] * 2),
                int(self.pacman.position[1] + pacman_dir[1] * 2)
            )
            self.destination = (
                intermediate[0] + (intermediate[0] - int(blinky.position[0])),
                intermediate[1] + (intermediate[1] - int(blinky.position[1]))
            )
        elif self.mode == "scatter":
            self.destination = self.scatter_point


class Clyde(Ghost):
    def __init__(self, position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman, scale: float):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        row = 7 * 16
        sprites = [
            [Sprite(atlas, pygame.Rect(0, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(1 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(2 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(3 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(4 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(5 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(6 * 16, row, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(7 * 16, row, 16, 16)).scale(scale)],
            [Sprite(atlas, pygame.Rect(8 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(9 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(10 * 16, 4 * 16, 16, 16)).scale(scale),
             Sprite(atlas, pygame.Rect(11 * 16, 4 * 16, 16, 16)).scale(scale)],
        ]
        super().__init__(sprites, position, direction, speed, arena, pacman)
        self.scatter_point = (0, len(self.arena.map) - 1)

    def update_destination(self):
        if self.mode == "chase":
            distance = ((self.position[0] - self.pacman.position[0]) ** 2 + 
                        (self.position[1] - self.pacman.position[1]) ** 2) ** 0.5
            if distance > 8:
                self.destination = (int(self.pacman.position[0]), int(self.pacman.position[1]))
            else:
                self.destination = self.scatter_point
        elif self.mode == "scatter":
            self.destination = self.scatter_point