import pygame
import sys
from gameobject import GameObject
from sprite import Sprite
from pygame.locals import (KEYDOWN, K_RIGHT, K_d, K_LEFT, K_a, K_UP, K_w, K_DOWN, K_s, K_ESCAPE)

class PacmanGame:

    def sprites_init(self):
        sprites = pygame.image.load('sprites/pacman_sprites.png')
        self.pacman = Sprite(sprites, pygame.Rect(32, 0, 16, 16))
        self.pacman.scale(self.scale)


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

    def render_sprite(self, sprite: Sprite, scale : int):
        hitbox = sprite.area.move(8 * scale, (8+16) * scale)
        
        

        self.screen.blit(sprite.texture, hitbox, sprite.area)


    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        
        self.render_sprite(self.pacman, 3)

    def update(self):
        pygame.display.update()
        # self.clock.tick(self.frame_rate)

    def proceed_event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                    self.playing = False



if __name__ == '__main__':
    pygame.init()
    game = PacmanGame(30, 232, 256, 3)
    
    while game.playing:
        game.proceed_event()
        game.render();
        game.update()

    pygame.quit()
    sys.exit()
