import pygame
from moveable import Moveable
from sprite import Sprite
from arena import Dot
from typing import Tuple

class Pacman(Moveable):
    def __init__(self, sprites: list[Sprite], position: tuple[int, int], direction: tuple[int, int], speed: float, arena):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena
        self.all_sprites = [sprites]  # Wrap single sprite list for compatibility
        self.lives: int = 3
        self.score: int = 0
        self.fruits: int = 0
        self.next_direction: Tuple[int, int] = direction
        self.animation_frame: float = 0.0
        self.animation_speed: float = 0.1
        self.game = None

    def rotate(self, direction: tuple[int, int]):
        self.next_direction = direction

    def can_move(self, direction: tuple[int, int]) -> bool:
        current_x, current_y = int(self.position[0]), int(self.position[1])
        next_x, next_y = current_x + direction[0], current_y + direction[1]
        # Allow movement across map edges for wrapping
        next_x = next_x % len(self.arena.map[0])
        next_y = next_y % len(self.arena.map)
        return self.arena.map[next_y][next_x] != Dot.WALL

    def update_position(self):
        x, y = self.position
        at_tile_center = abs(x - int(x)) < 0.1 and abs(y - int(y)) < 0.1

        # Check for dot collection
        current_x, current_y = int(x), int(y)
        if (0 <= current_y < len(self.arena.map) and 
            0 <= current_x < len(self.arena.map[0])):
            dot_type = self.arena.map[current_y][current_x]
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
                self.arena.remove_dot((current_x, current_y))

        # Get map dimensions
        map_width = len(self.arena.map[0])
        map_height = len(self.arena.map)

        # Update position
        if not at_tile_center:
            new_position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
            x, y = new_position
            # Wrap around
            if x < 0:
                x += map_width
            elif x >= map_width:
                x -= map_width
            if y < 0:
                y += map_height
            elif y >= map_height:
                y -= map_height
            self.position = (x, y)
        else:
            self.position = (int(x + 0.5), int(y + 0.5))
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
            elif not self.can_move(self.direction):
                self.direction = (0, 0)
            if self.direction != (0, 0) and self.can_move(self.direction):
                new_position = tuple(map(lambda x, y: x + y * self.speed, self.position, self.direction))
                x, y = new_position
                # Wrap around
                if x < 0:
                    x += map_width
                elif x >= map_width:
                    x -= map_width
                if y < 0:
                    y += map_height
                elif y >= map_height:
                    y -= map_height
                self.position = (x, y)

    def get_sprite(self) -> Sprite:
        # Cycle through 3 sprites for animation
        if self.direction != (0, 0):
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(self.sprites)
        else:
            self.animation_frame = 0  # Show first sprite when stationary
        
        # Get base sprite
        base_sprite = self.sprites[int(self.animation_frame)]
        
        # Rotate sprite based on direction
        if self.direction == (1, 0):  # Right (default, no rotation)
            return base_sprite
        elif self.direction == (-1, 0):  # Left (flip horizontally)
            rotated_texture = pygame.transform.flip(base_sprite.texture, True, False)
            return Sprite(rotated_texture, base_sprite.area.copy())
        elif self.direction == (0, -1):  # Up (rotate 90° counterclockwise)
            rotated_texture = pygame.transform.rotate(base_sprite.texture, 90)
            return Sprite(rotated_texture, pygame.Rect(0, 0, base_sprite.area.h, base_sprite.area.w))
        elif self.direction == (0, 1):  # Down (rotate 90° clockwise)
            rotated_texture = pygame.transform.rotate(base_sprite.texture, -90)
            return Sprite(rotated_texture, pygame.Rect(0, 0, base_sprite.area.h, base_sprite.area.w))
        return base_sprite  # Fallback to default if direction is (0, 0)

    def get_hitbox(self) -> pygame.Rect:
        sprite = self.get_sprite()
        return pygame.Rect(
            self.position[0] * sprite.area.w / 2,
            self.position[1] * sprite.area.h / 2,
            sprite.area.w,
            sprite.area.h
        )

    def update_destination(self):
        pass  # Not used

    def move(self, map):
        self.update_position()  # Redirect to update_position

