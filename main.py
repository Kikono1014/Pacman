import pygame
import sys
from gameobject import GameObject
from sprite import Sprite
from pygame.locals import (KEYDOWN, K_RIGHT, K_d, K_LEFT, K_a, K_UP, K_w, K_DOWN, K_s, K_ESCAPE)

class PacmanGame:

    def sprites_init(self):
        sprites = pygame.image.load('sprites/pacman_sprites.png')
        self.pacman = Sprite(sprites, pygame.Rect(32, 0, 16, 16))


    def __init__(self, frame_rate, width, height):
        self.frame_rate = frame_rate
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.background = pygame.image.load('sprites/pacman_background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        pygame.display.set_caption("Pacman")

        self.sprites_init()

        self.playing = True
        self.game_over = False

    def render_sprite(self, sprite: Sprite, scale : int):
        hitbox = (8 * scale, (8+16) * scale, sprite.area.w * scale, sprite.area.h * scale)
        
        texture = pygame.transform.scale(sprite.texture, (sprite.texture.get_width() * scale, sprite.texture.get_height() * scale))
        self.screen.blit(texture, hitbox, (sprite.area.x * scale, sprite.area.y * scale, 16 * scale, 16 * scale))


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
            if e.type == pygame.VIDEORESIZE:
                self.width, self.height = e.w, e.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
                self.background = pygame.transform.scale(self.background, (self.width, self.height))



if __name__ == '__main__':
    pygame.init()
    game = PacmanGame(30, 232*3, 256*3)
    
    while game.playing:
        game.proceed_event()
        game.render();
        game.update()

    pygame.quit()
    sys.exit()
