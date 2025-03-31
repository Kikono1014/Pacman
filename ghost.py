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
        self.mode_duration = 600  # 10 секунд при 60 FPS

        self.sprites = sprites


    def get_sprite(self):
        #TODO fix modes
        if (self.mode == "scatter"):
            directionID = None
            if (self.direction[0] == 1 and self.direction[1] == 0):
                directionID = 0
            if (self.direction[0] == -1 and self.direction[1] == 0):
                directionID = 1
            if (self.direction[0] == 0 and self.direction[1] == -1):
                directionID = 2
            if (self.direction[0] == 0 and self.direction[1] == 1):
                directionID = 3
            
            self.current = (self.current + 1) % 2

            return self.sprites[directionID][self.current]
        elif (self.mode == "frightened"):
            self.current = (self.current + 1) % 4
            return self.sprites[4][self.current]



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
        self.frightened_timer = 60
        self.change_sprite(1)

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

        if self.mode != "frightened":
            self.mode_timer += 1
            if self.mode_timer >= self.mode_duration:
                self.mode_timer = 0
                self.mode = "chase" if self.mode == "scatter" else "scatter"

        self.update_destination()
        if self.mode == "frightened":
            self.speed = self.base_speed * 0.5
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "scatter"
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for direction in directions:
                if self.can_move(direction):
                    self.rotate(direction)
                    super().move()
                    break
        else:
            self.speed = self.base_speed
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            best_direction = self.direction
            min_distance = float("inf")

            for direction in directions:
                if self.can_move(direction):
                    next_pos = tuple(map(sum, zip(self.position, direction)))
                    distance = ((next_pos[0] - self.destination[0]) ** 2 + 
                                (next_pos[1] - self.destination[1]) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = direction

            self.rotate(best_direction)
            if self.can_move(self.direction):
                super().move()

        if self.check_collision(self.pacman):
            if self.mode == "frightened":
                self.position = self.arena.ghost_start
                self.is_active = False
                self.respawn_timer = 120
            else:
                self.pacman.position = self.arena.pacman_start