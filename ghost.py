from moveable import Moveable
from sprite import Sprite
from arena import Dot
import heapq

class Ghost(Moveable):
    def __init__(self, sprites: list[list[Sprite]], position: tuple[int, int], direction: tuple[int, int], speed: float, arena, pacman):
        super().__init__(sprites[0], position, direction, speed)
        self.arena = arena
        self.pacman = pacman
        self.game = pacman.game
        self.destination: tuple[int, int] = position
        self.mode = "scatter"
        self.frightened_timer = 0
        self.base_speed = speed
        self.respawn_timer = 0
        self.is_active = True
        self.mode_timer = 0
        self.mode_duration = 600  # 10 секунд при 60 FPS
        self.sprites = sprites
        
        # Додаткові параметри для A*
        self.path = []
        self.path_update_timer = 0
        self.path_update_interval = 10  # Оновлювати шлях кожні 10 кадрів

    def get_sprite(self):
        if self.mode == "frightened":
            self.current = (self.current + 1) % 4
            return self.sprites[4][self.current]
        else:
            directionID = { 
                (1, 0): 0,   # right
                (-1, 0): 1,  # left
                (0, -1): 2,  # up
                (0, 1): 3    # down
            }.get(self.direction, 0)
            self.current = (self.current + 1) % 2
            return self.sprites[directionID][self.current]

    def can_move(self, direction: tuple[int, int]) -> bool:
        next_pos = tuple(map(sum, zip(self.position, direction)))
        x, y = int(next_pos[0]), int(next_pos[1])
        if not (0 <= y < len(self.arena.map) and 0 <= x < len(self.arena.map[0])):
            return False
        if self.arena.map[y][x] == Dot.WALL:
            return False
        # Перевірка на зіткнення з іншими привидами
        for other_ghost in self.game.ghosts:
            if other_ghost != self and other_ghost.is_active:
                other_x, other_y = int(other_ghost.position[0]), int(other_ghost.position[1])
                if other_x == x and other_y == y:
                    return False
        return True

    def heuristic(self, pos: tuple[int, int], target: tuple[int, int]) -> float:
        """Евклідова відстань як евристика для A*"""
        return ((pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2) ** 0.5

    def find_path(self, start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
        """A* алгоритм пошуку шляху"""
        start = (int(start[0]), int(start[1]))
        target = (int(target[0]), int(target[1]))
        
        queue = [(0, start, [])]
        visited = set()
        
        while queue:
            f_score, current, path = heapq.heappop(queue)
            
            if current == target:
                return path + [current]
                
            if current in visited:
                continue
                
            visited.add(current)
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                next_pos = (current[0] + dx, current[1] + dy)
                if self.can_move((dx, dy)) and next_pos not in visited:
                    g_score = len(path) + 1
                    h_score = self.heuristic(next_pos, target)
                    f_score = g_score + h_score
                    heapq.heappush(queue, (f_score, next_pos, path + [current]))
        
        # Якщо шлях не знайдено, повертаємо прямий рух до цілі
        return [start, target]

    def update_destination(self):
        """Цей метод буде перевизначений у дочірніх класах"""
        pass

    def move(self):
        if not self.is_active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_active = True
                self.mode = "scatter"
            return

        # Оновлення режиму
        if self.mode != "frightened":
            self.mode_timer += 1
            if self.mode_timer >= self.mode_duration:
                self.mode_timer = 0
                self.mode = "chase" if self.mode == "scatter" else "scatter"

        # Оновлення шляху
        self.path_update_timer += 1
        if self.path_update_timer >= self.path_update_interval or not self.path:
            self.update_destination()
            self.path = self.find_path(self.position, self.destination)
            self.path_update_timer = 0

        # Рух по шляху
        if self.mode == "frightened":
            self.speed = self.base_speed * 0.5
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "scatter"
                
            # Випадковий рух у режимі страху
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_directions = [d for d in directions if self.can_move(d)]
            if valid_directions:
                # Вибираємо напрямок, протилежний до поточного
                opposite = (-self.direction[0], -self.direction[1])
                valid_directions = [d for d in valid_directions if d != opposite] or valid_directions
                self.rotate(valid_directions[0])
                super().move()
        else:
            self.speed = self.base_speed
            if self.path and len(self.path) > 1:
                next_pos = self.path[1]
                direction = (next_pos[0] - int(self.position[0]), 
                           next_pos[1] - int(self.position[1]))
                if self.can_move(direction):
                    self.rotate(direction)
                    super().move()
                    # Видаляємо пройдену точку
                    if (int(self.position[0]), int(self.position[1])) == next_pos:
                        self.path.pop(0)

        # Перевірка зіткнення з PacMan
        if self.check_collision(self.pacman):
            if self.mode == "frightened":
                self.position = self.arena.ghost_start
                self.is_active = False
                self.respawn_timer = 120
                self.path = []
            else:
                self.pacman.position = self.arena.pacman_start

    def check_collision(self, pacman):
        pacman_hitbox = pacman.get_hitbox()
        ghost_hitbox = self.get_hitbox()
        return pacman_hitbox.colliderect(ghost_hitbox)

    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 420  # 7 секунд при 60 FPS
        self.path = []