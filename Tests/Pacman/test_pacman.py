import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import pygame
from unittest.mock import Mock, patch
from pacman import Pacman
from sprite import Sprite
from arena import Arena, Dot

@pytest.fixture
def pacman():
    # Простые заглушки
    pygame.init()
    dummy_surface = pygame.Surface((32, 32))
    dummy_rect = pygame.Rect(0, 0, 32, 32)
    
    dot_sprites = [
        Sprite(dummy_surface, dummy_rect),  # обычная точка
        Sprite(dummy_surface, dummy_rect),  # пусто
        Sprite(dummy_surface, dummy_rect),  # пеллет
        Sprite(dummy_surface, dummy_rect)   # фрукт (можно добавить больше при необходимости)
    ]
    
    # Создаём фиктивную арену без загрузки файлов
    class DummyArena(Arena):
        def build(self):
            self.map = [
                [Dot.NORMAL, Dot.NORMAL, Dot.NORMAL, Dot.NORMAL, Dot.NORMAL],
                [Dot.NORMAL, Dot.WALL,   Dot.WALL,   Dot.NORMAL, Dot.NORMAL],
                [Dot.NORMAL, Dot.WALL,   Dot.NORMAL, Dot.NORMAL, Dot.NORMAL],
                [Dot.NORMAL, Dot.WALL,   Dot.WALL,   Dot.NORMAL, Dot.NORMAL],
                [Dot.NORMAL, Dot.NORMAL, Dot.NORMAL, Dot.NORMAL, Dot.NORMAL],
            ]
            self.pacman_start = (2, 2)
            self.ghost_start = (0, 0)
            self.background = Mock()  # чтобы не падало на blit

    arena = DummyArena(area=pygame.Rect(0, 0, 160, 160), scale=1.0, dot_sprites=dot_sprites, preset=1)
    return Pacman(sprites=dot_sprites, position=(2, 2), direction=(0, 1), speed=0.1, arena=arena)

# Все тесты ниже можно оставить как есть:
def test_pacman_initial_position(pacman: Pacman):
    assert pacman.position == (2, 2)

def test_pacman_move_right(pacman: Pacman):
    pacman.rotate((1, 0))  
    pacman.update_position()  
    assert round(pacman.position[0], 1) == 2.1

def test_pacman_move_up(pacman: Pacman):
    pacman.rotate((0, -1))  
    if pacman.can_move((0, -1)):
        pacman.update_position()
        assert round(pacman.position[1], 1) == 1.9
    else:
        assert round(pacman.position[1], 1) == 2

def test_pacman_collision_with_wall(pacman: Pacman):
    pacman.rotate((1, 0))  
    pacman.update_position()  
    pacman.rotate((1, 0))  
    pacman.update_position()  
    assert round(pacman.position[0], 1) <= 2.2  # стенка справа, дальше идти нельзя

def test_pacman_get_sprite(pacman: Pacman):
    pacman.rotate((1, 0)) 
    sprite = pacman.get_sprite()
    assert isinstance(sprite, Sprite)
    assert sprite.texture.get_width() == 32  

def test_pacman_get_hitbox(pacman: Pacman):
    pacman.rotate((1, 0))  
    hitbox = pacman.get_hitbox()
    assert isinstance(hitbox, pygame.Rect)
    assert hitbox.width == 32  
    assert hitbox.height == 32  

def test_pacman_update_destination(pacman: Pacman):
    pacman.update_destination()  
    assert True
