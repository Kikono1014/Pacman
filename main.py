import pygame
import sys
import os
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

        self.sprites["live"] = self.sprites["pacman"][0]

    def play_opening(self):
        pygame.mixer.music.set_endevent(self.OPENING_END_EVENT)
        self.sounds["OpeningSong"] = pygame.mixer.music.load(os.getcwd() + "/sounds/" + "OpeningSong.wav");
        pygame.mixer.music.play()
        self.opening = True


    def sounds_init(self):
        path = os.getcwd() + "/sounds/";
        self.sounds["Dies"] = pygame.mixer.Sound(path + "Dies.wav");
        self.sounds["EatingCherry"] = pygame.mixer.Sound(path + "EatingCherry.wav");
        self.sounds["EatingGhost"] = pygame.mixer.Sound(path + "EatingGhost.wav");
        self.sounds["ExtraLive"] = pygame.mixer.Sound(path + "ExtraLive.wav");
        self.sounds["Intermission"] = pygame.mixer.Sound(path + "Intermission.wav");
        
        self.OPENING_END_EVENT = pygame.USEREVENT + 1
        self.play_opening()



        self.sounds["Siren"] = pygame.mixer.Sound(path + "Siren.wav");
        
        self.sounds["WakaWaka"] = pygame.mixer.Sound(path + "WakaWaka.wav");
        self.sounds["WakaWaka1"] = pygame.mixer.Sound(path + "WakaWaka1.wav");
    
        self.waka = 1
    
    

    def ghosts_init(self):
        self.ghosts = [
            Blinky(self.arena.ghost_start, (0, 1), 0.09, self.arena, self.pacman, self.scale),
            Pinky(self.arena.ghost_start, (0, -1), 0.09, self.arena, self.pacman, self.scale),
            Inky(self.arena.ghost_start, (-1, 0), 0.09, self.arena, self.pacman, self.scale),
            Clyde(self.arena.ghost_start, (1, 0), 0.09, self.arena, self.pacman, self.scale),
        ]
        for ghost in self.ghosts:
            ghost.game = self
            ghost.mode = "scatter"


    def __init__(self, frame_rate, width, height, scale, preset):
        self.frame_rate = frame_rate
        self.scale = scale
        self.preset = preset
        self.width = width * self.scale
        self.height = (height + 20) * self.scale

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.sprites = {}
        self.sprites_init()

        self.sounds = {}
        self.sounds_init()

        self.arena = Arena(pygame.Rect(0, 0, width, height), scale, self.sprites["dot_sprites"], preset)

        self.pacman = Pacman(self.sprites["pacman"], self.arena.pacman_start, (1, 0), 0.108, self.arena)
        self.pacman.game = self

        self.ghosts_init()

        self.score = 0
        self.high_score = 0 # best result

        self.extra_life_given = False

        self.playing = True
        self.game_over = False
        self.game_won = False

    def render_object(self, object: GameObject):
        sprite = object.get_sprite()
        self.screen.blit(sprite.texture, object.get_hitbox(), sprite.area)

    def render_lives(self):
        y = self.height - self.sprites["live"].texture.get_height() - 10
        for i in range(self.pacman.lives):
            x = 10 + i * (self.sprites["live"].texture.get_width() + 10)
            self.screen.blit(self.sprites["live"].texture, (x, y), self.sprites["live"].area)

    def render_score(self):
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Score: {self.pacman.score} Fruits: {self.pacman.fruits}", True, (255, 255, 255))
        x = self.width - text.get_width() - 10
        y = self.height - self.sprites["live"].texture.get_height() - 10
        self.screen.blit(text, (x, y))

    def render_game_over(self):
        font = pygame.font.SysFont("Arial", 48, bold=True)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(game.width // 2, game.height // 2))
        
        # Отображаем сообщение для перезапуска
        restart_text = pygame.font.SysFont("Arial", 24).render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(game.width // 2, game.height // 2 + 50))
        
        surface_rect = pygame.Rect(restart_rect.left, text_rect.top,
                                    restart_rect.width,
                                    text_rect.height + restart_rect.height)
        surface = pygame.Surface((surface_rect.w, surface_rect.h))
        surface.fill((0, 0, 0))

        game.screen.blit(surface, surface_rect)
        game.screen.blit(restart_text, restart_rect)
        game.screen.blit(game_over_text, text_rect)

    def render_game_won(self):
        font = pygame.font.SysFont("Arial", 48, bold=True)
        game_won_text = font.render("Game Won", True, (0, 255, 0))
        text_rect = game_won_text.get_rect(center=(game.width // 2, game.height // 2))
        
        # Отображаем сообщение для перезапуска
        restart_text = pygame.font.SysFont("Arial", 24).render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(game.width // 2, game.height // 2 + 50))
        
        surface_rect = pygame.Rect(restart_rect.left, text_rect.top,
                                    restart_rect.width,
                                    text_rect.height + restart_rect.height)
        surface = pygame.Surface((surface_rect.w, surface_rect.h))
        surface.fill((0, 0, 0))

        game.screen.blit(surface, surface_rect)
        game.screen.blit(restart_text, restart_rect)
        game.screen.blit(game_won_text, text_rect)


    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.arena.background.texture, (0, 0))
        self.render_object(self.pacman)
        for ghost in self.ghosts:
            if ghost.is_active:
                self.render_object(ghost)
        
        # Отображаем счёт и количество фруктов
        self.render_score()

        self.render_lives()

        # Если игра завершена, показываем сообщение "GAME OVER"
        if (self.game_over):
            self.render_game_over()
        
        if (self.game_won):
            self.render_game_won()

        pygame.display.update()

    def update(self):
        if (self.opening):
            return
        
        self.pacman.update_position()

        x, y = int(self.pacman.position[0]), int(self.pacman.position[1])
        current_dot = self.arena.map[y][x]

        if current_dot == Dot.NORMAL:
            self.pacman.score += 10

            if (self.waka == 1):
                self.sounds["WakaWaka"].play()
                self.waka = 0;
            else:
                self.sounds["WakaWaka1"].play()
                self.waka = 1

        elif current_dot == Dot.PELLET:
            self.pacman.score += 50

            # Перевести всех призраков в frightened режим
            for ghost in self.ghosts:
                ghost.set_frightened()

        elif current_dot == Dot.FRUIT:
            self.pacman.score += 1000
            self.pacman.fruits += 1
            self.sounds["EatingCherry"].play()

        
        self.arena.remove_dot((x, y))

        # Добавляем фрукты в игру
        empty_count = len(self.arena.get_dots(Dot.EMPTY))
        fruit_count = len(self.arena.get_dots(Dot.FRUIT))
        if empty_count > 80 and fruit_count == 0 and randint(0, 100) == 20:
            self.arena.add_fruit(self.pacman.fruits)

        if (len(self.arena.get_dots(Dot.NORMAL)) == 0):
            self.game_won = True

        for ghost in self.ghosts:
            ghost.move(self.arena.map)
            if ghost.check_collision(self.pacman):
                if ghost.mode == "frightened":
                    ghost.mode = "chase"
                    ghost.position = tuple(map(sum, zip(self.arena.ghost_start , (0, 2))))
                    ghost.is_active = False
                    ghost.respawn_timer = 120  # 2 секунды при 60 FPS
                    self.pacman.score += 200
                    self.sounds["EatingGhost"].play()
                    
                elif ghost.is_active:
                    self.pacman.lives -= 1
                    self.pacman.position = self.arena.pacman_start
                    self.pacman.direction = (1, 0)
                    self.pacman.next_direction = (1, 0)
                    if self.pacman.lives <= 0:
                        self.game_over = True
                        pygame.mixer.pause()
                        self.sounds["Dies"].play()


        if (self.pacman.score >= 10_000 and self.extra_life_given == False):
            self.extra_life_given = True
            self.pacman.lives += 1
            self.sounds["ExtraLive"].play()

        self.clock.tick(self.frame_rate)

    def proceed_event(self):
        for e in pygame.event.get():
            if e.type == self.OPENING_END_EVENT:
                self.opening = False;
                self.sounds["Siren"].play(loops=-1)
                pygame.mixer.unpause()
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
                if e.key == pygame.K_r:  # Перезапуск при нажатии R
                    self.arena.build()
                    self.pacman = Pacman(self.sprites["pacman"], self.arena.pacman_start, (1, 0), 0.108, self.arena)
                    self.pacman.game = self
                    self.ghosts_init()
                    self.play_opening()
                    self.extra_life_given = False
                    self.playing = True
                    self.game_over = False
                    self.game_won = False

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    preset = 1
    scale = 2
    if len(sys.argv) >= 2:
        preset = int(sys.argv[1])
    if len(sys.argv) >= 3:
        scale = int(sys.argv[2])

    game = PacmanGame(60, 232, 256, scale, preset)

    while game.playing:  # Игра будет продолжаться, пока игрок не решит выйти
        game.proceed_event()  # Обрабатываем события

        # Если игра не завершена, обновляем её
        if not game.game_over:
            game.update()

        # Отображаем игру (счёт, персонажа, призраков и т.д.)
        game.render()



    pygame.quit()
    sys.exit()


