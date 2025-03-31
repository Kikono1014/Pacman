import pygame
import sys
from sprite import Sprite
from gameobject import GameObject
from moveable import Moveable
from arena import Arena
from arena import Dot
from ghosts import Blinky, Pinky, Inky, Clyde  # Оновлений імпорт

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
        self.width  = width  * self.scale
        self.height = height * self.scale

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)

        self.sprites = {}
        self.sprites_init()

        self.arena = Arena(pygame.Rect(0, 0, width, height), scale, self.sprites["dot_sprites"], preset)

        #! Test objects
        self.pacman = Moveable(self.sprites["pacman"], self.arena.pacman_start, (0, 1), 1.08)
        self.pacman.change_sprite(2)
        self.pacman.game = self

        self.ghosts = [
            Blinky(self.arena.ghost_start, (0, 1), 1.0, self.arena, self.pacman, self.scale),
            Pinky(self.arena.ghost_start, (0, -1), 0.9, self.arena, self.pacman, self.scale),
            Inky(self.arena.ghost_start, (-1, 0), 0.8, self.arena, self.pacman, self.scale),
            Clyde(self.arena.ghost_start, (1, 0), 0.7, self.arena, self.pacman, self.scale),
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

    def update(self):
        prev_position = self.pacman.position  # Сохраняем предыдущую позицию
        self.pacman.move(self.arena)  # Передаём арену в move()

        if self.arena.map[self.pacman.position[1]][self.pacman.position[0]] == Dot.WALL:
            self.pacman.position = prev_position 

        pygame.display.update()
        #!
        self.clock.tick(self.frame_rate)


    def proceed_event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                    self.playing = False
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    self.pacman.rotate((0, -1), self.arena)
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    self.pacman.rotate((-1, 0), self.arena)
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    self.pacman.rotate((0, 1), self.arena)
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    self.pacman.rotate((1, 0), self.arena)



if __name__ == '__main__':
    pygame.init()
    preset = 1
    scale = 2
    if len(sys.argv) >= 2:
        preset = int(sys.argv[1])
    if len(sys.argv) >= 3:
        scale = int(sys.argv[2])
    game = PacmanGame(10, 232, 256, scale, preset)
    while game.playing:
        game.proceed_event()
        game.render();
        game.update()
    pygame.quit()
    sys.exit()
