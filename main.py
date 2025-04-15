import pygame
import sys
from sprite import Sprite
from gameobject import GameObject
from moveable import Moveable
from arena import Arena, Dot
from ghosts import Blinky, Pinky, Inky, Clyde
from pacman import Pacman
from random import randint

class PacmanGame:
    def sprites_init(self):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        dot_sprites = [
            Sprite(atlas, pygame.Rect(10 * 16, 3 * 16, 16, 16)).scale(self.scale),  # Normal dot
            Sprite(atlas, pygame.Rect(12 * 16, 3 * 16, 16, 16)).scale(self.scale),  # Empty
            Sprite(atlas, pygame.Rect(11 * 16, 3 * 16, 16, 16)).scale(self.scale),  # Pellet
        ]
        for i in range(2, 10):  # Fruits
            dot_sprites.append(
                Sprite(atlas, pygame.Rect(i * 16, 3 * 16, 16, 16)).scale(self.scale)
            )
        self.sprites["dot_sprites"] = dot_sprites
        
        # Pacman sprites: 3 frames (no directional sprites, as in Code #2)
        self.sprites["pacman"] = [
            Sprite(atlas, pygame.Rect(0 * 16, 0 * 16, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(1 * 16, 0 * 16, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(2 * 16, 0 * 16, 16, 16)).scale(self.scale),
        ]

    def __init__(self, frame_rate, width, height, scale, preset):
        self.frame_rate = frame_rate
        self.scale = scale
        self.width = width * self.scale
        self.height = height * self.scale

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.sprites = {}
        self.sprites_init()

        self.arena = Arena(pygame.Rect(0, 0, width, height), scale, self.sprites["dot_sprites"], preset)

        self.pacman = Pacman(self.sprites["pacman"], self.arena.pacman_start, (1, 0), 0.108, self.arena)

        self.pacman.game = self

        self.score = 0
        self.high_score = 0 # best result

        self.ghosts = [
            Blinky(self.arena.ghost_start, (0, 1), 0.09, self.arena, self.pacman, self.scale),
            Pinky(self.arena.ghost_start, (0, -1), 0.09, self.arena, self.pacman, self.scale),
            Inky(self.arena.ghost_start, (-1, 0), 0.09, self.arena, self.pacman, self.scale),
            Clyde(self.arena.ghost_start, (1, 0), 0.09, self.arena, self.pacman, self.scale),
        ]
        for ghost in self.ghosts:
            ghost.game = self
            ghost.mode = "scatter"

        self.playing = True
        self.game_over = False

    def render_object(self, object: GameObject):
        sprite = object.get_sprite()
        self.screen.blit(sprite.texture, object.get_hitbox(), sprite.area)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.arena.background.texture, (0, 0))
        self.render_object(self.pacman)
        for ghost in self.ghosts:
            if ghost.is_active:
                self.render_object(ghost)
        
        # ���������� ���� � ���������� �������
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.pacman.score}", True, (255, 255, 255))
        fruits_text = font.render(f"Fruits: {self.pacman.fruits}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # ����
        self.screen.blit(fruits_text, (10, 50))  # ���������� �������

        pygame.display.update()

    def update(self):
        self.pacman.update_position()

        x, y = int(self.pacman.position[0]), int(self.pacman.position[1])
        current_dot = self.arena.map[y][x]

        if current_dot == Dot.NORMAL:
            self.pacman.score += 10
            self.arena.remove_dot((x, y))

        elif current_dot == Dot.PELLET:
            self.pacman.score += 50
            self.arena.remove_dot((x, y))
            # ��������� ���� ��������� � frightened �����
            for ghost in self.ghosts:
                ghost.set_frightened()

        elif current_dot == Dot.FRUIT:
            self.pacman.score += 100
            self.pacman.fruits += 1
            self.arena.remove_dot((x, y))

        # ��������� ������ � ����
        empty_count = len(self.arena.get_dots(Dot.EMPTY))
        fruit_count = len(self.arena.get_dots(Dot.FRUIT))
        if empty_count > 80 and fruit_count == 0 and randint(0, 100) == 20:
            self.arena.add_fruit(self.pacman.fruits)

        for ghost in self.ghosts:
            ghost.move(self.arena.map)
            if ghost.check_collision(self.pacman):
                if ghost.mode == "frightened":
                    ghost.position = self.arena.ghost_start
                    ghost.is_active = False
                    ghost.respawn_timer = 120  # 2 ������� ��� 60 FPS
                    self.pacman.score += 200
                elif ghost.is_active:
                    self.pacman.lives -= 1
                    self.pacman.position = self.arena.pacman_start
                    if self.pacman.lives <= 0:
                        self.game_over = True

        self.clock.tick(self.frame_rate)

    def proceed_event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                    self.playing = False
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    self.pacman.rotate((0, -1))
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    self.pacman.rotate((-1, 0))
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    self.pacman.rotate((0, 1))
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    self.pacman.rotate((1, 0))

if __name__ == '__main__':
    pygame.init()
    preset = 1
    scale = 2
    if len(sys.argv) >= 2:
        preset = int(sys.argv[1])
    if len(sys.argv) >= 3:
        scale = int(sys.argv[2])
    game = PacmanGame(60, 232, 256, scale, preset)
    while game.playing:
        game.proceed_event()
        game.render()
        game.update()

    pygame.quit()
    sys.exit()
