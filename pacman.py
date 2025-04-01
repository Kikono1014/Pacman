import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot

class PacMan(Moveable):
    def __init__(self, sprites: list[Sprite], position: tuple[int, int], direction: tuple[int, int], speed: float, arena):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena
        self.next_direction = direction  # Намір руху
        self.score = 0  # Очки гравця

    def get_sprite(self):
        # Завжди повертаємо перший (і єдиний) спрайт
        return self.sprites[0]

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        if 0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0]):
            return self.arena.map[y][x] != Dot.WALL
        return False

    def update(self):
        # Перевірка наміру руху
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        # Рух, якщо можливо
        prev_position = self.position
        next_pos = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
        self.position = next_pos

        # Перевірка на стіну
        if not self.can_move((0, 0)):  # Перевірка поточної позиції
            self.position = prev_position

        # Перевірка на поїдання кульок
        pacman_pos = (int(self.position[0]), int(self.position[1]))
        if 0 <= pacman_pos[1] < len(self.arena.map) and 0 <= pacman_pos[0] < len(self.arena.map[0]):
            if self.arena.map[pacman_pos[1]][pacman_pos[0]] == Dot.PELLET:
                self.arena.map[pacman_pos[1]][pacman_pos[0]] = Dot.EMPTY
                self.arena.objects[pacman_pos[1]][pacman_pos[0]].change_sprite(0)
                self.score += 10  # Додаємо очки за кульку
                for ghost in self.game.ghosts:
                    ghost.set_frightened()
            elif self.arena.map[pacman_pos[1]][pacman_pos[0]] == Dot.NORMAL:
                self.arena.map[pacman_pos[1]][pacman_pos[0]] = Dot.EMPTY
                self.arena.objects[pacman_pos[1]][pacman_pos[0]].change_sprite(0)
                self.score += 1  # Додаємо очки за звичайну точку

    def rotate(self, direction: tuple[int, int]):
        self.next_direction = direction  # Змінюємо намір руху