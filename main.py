import pygame
import sys
from sprite import Sprite
from gameobject import GameObject
from moveable import Moveable
from pygame.locals import (KEYDOWN, K_RIGHT, K_d, K_LEFT, K_a, K_UP, K_w, K_DOWN, K_s, K_ESCAPE)

class PacmanGame:

    def sprites_init(self):
        sprites = pygame.image.load('sprites/pacman_sprites.png')

        #! Test objects
        sprite = Sprite(sprites, pygame.Rect(32, 0, 16, 16)).scale(self.scale)
        self.pacman = Moveable([sprite], (0, 0), (0, 1), 1.08)
        
        sprite = Sprite(sprites, pygame.Rect(10 * 16, 3 * 16, 16, 16)).scale(self.scale)
        self.dot = GameObject([sprite], (0, 0))

        sprite = Sprite(sprites, pygame.Rect(10 * 16, 3 * 16, 16, 16)).scale(self.scale)
        self.dot1 = GameObject([sprite], (1, 0))

        sprite = Sprite(sprites, pygame.Rect(10 * 16, 3 * 16, 16, 16)).scale(self.scale)
        self.dot2 = GameObject([sprite], (0, 1))

        sprite = Sprite(sprites, pygame.Rect(11 * 16, 3 * 16, 16, 16)).scale(self.scale)
        self.bonus = GameObject([sprite], (0, 2))

        #!




    def __init__(self, frame_rate, width, height, scale):
        self.frame_rate = frame_rate
        self.width = width * scale
        self.height = height * scale

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.background = pygame.image.load('sprites/pacman_background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        pygame.display.set_caption("Pacman")

        self.scale = scale

        self.sprites_init()

        self.playing = True
        self.game_over = False

    def render_object(self, object: GameObject):
        self.screen.blit(object.get_sprite().texture, object.get_hitbox(), object.get_sprite().area)


    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        
        #! Test objects
        self.render_object(self.pacman)
        self.render_object(self.dot)
        self.render_object(self.dot1)
        self.render_object(self.dot2)
        self.render_object(self.bonus)
        #!

    def update(self):
        pygame.display.update()
        self.pacman.move()

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
    game = PacmanGame(48, 232, 256, 4)
    
    while game.playing:
        game.proceed_event()
        game.render();
        game.update()

    pygame.quit()
    sys.exit()
