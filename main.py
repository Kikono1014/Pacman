import pygame
import sys
from sprite import Sprite
from arena import Arena
from pacman import PacMan
from ghosts import Blinky, Pinky, Inky, Clyde
from gameobject import GameObject

class PacmanGame:
    def sprites_init(self):
        atlas = pygame.image.load('sprites/pacman_sprites.png')
        dot_sprites = [
            Sprite(atlas, pygame.Rect(10 * 16, 3 * 16, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(12 * 16, 3 * 16, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(11 * 16, 3 * 16, 16, 16)).scale(self.scale),
        ]
        for i in range(2, 10):
            dot_sprites.append(
                Sprite(atlas, pygame.Rect(i * 16, 3 * 16, 16, 16)).scale(self.scale)
            )
        self.sprites["dot_sprites"] = dot_sprites
        
        self.sprites["pacman"] = [
            Sprite(atlas, pygame.Rect(0 * 16, 0, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(1 * 16, 0, 16, 16)).scale(self.scale),
            Sprite(atlas, pygame.Rect(2 * 16, 0, 16, 16)).scale(self.scale)
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

        self.pacman = PacMan(self.sprites["pacman"], self.arena.pacman_start, (0, 1), 0.108)
        self.pacman.game = self

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

    def render_arena(self):
        for y in range(len(self.arena.map)):
            for x in range(len(self.arena.map[0])):
                self.render_object(self.arena.objects[y][x])

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.arena.background.texture, (0, 0))
        self.render_arena()

        self.render_object(self.pacman)
        for ghost in self.ghosts:
            if ghost.is_active:
                self.render_object(ghost)

        pygame.display.update()

    def update(self):
        self.pacman.update_position()

        for ghost in self.ghosts:
            ghost.move()
            if ghost.check_collision(self.pacman):
                if ghost.mode == "frightened":
                    ghost.position = self.arena.ghost_start
                    ghost.is_active = False
                    ghost.respawn_timer = 120  # 2 seconds at 60 FPS
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