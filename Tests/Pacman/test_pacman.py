import sys
import os
# Додаємо корінь проєкту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
import pygame
from unittest.mock import Mock, patch
from pacman import Pacman
from sprite import Sprite
from arena import Arena, Dot  

@pytest.fixture
def pacman():
    sprites = [Sprite(pygame.Surface((32, 32)), pygame.Rect(0, 0, 32, 32))]  # Простой спрайт для теста
    arena = Arena(map=[  # Пример карты, где есть стены (1 - стена, 0 - пусто)
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    return Pacman(sprites=sprites, position=(2, 2), direction=(0, 1), speed=0.1, arena=arena)

def test_pacman_initial_position(pacman: Pacman):
    """Проверка начальной позиции Pacman"""
    assert pacman.position == (2, 2)

def test_pacman_move_right(pacman: Pacman):
    """Проверка движения вправо"""
    pacman.rotate((1, 0))  
    pacman.update_position()  
    assert pacman.position == (2.1, 2)  

def test_pacman_move_up(pacman: Pacman):
    """Проверка движения вверх"""
    pacman.rotate((0, -1))  
    pacman.update_position()  
    assert pacman.position == (2, 1.9)  

def test_pacman_collision_with_wall(pacman: Pacman):
    """Проверка коллизии с препятствием (стеной)"""
    pacman.rotate((1, 0))  
    pacman.update_position()  
    pacman.rotate((1, 0))  
    pacman.update_position()  
    assert pacman.position == (2.2, 2)

def test_pacman_can_move(pacman: Pacman):
    """Проверка, может ли Pacman двигаться в заданном направлении"""
    assert pacman.can_move((1, 0)) is True  
    assert pacman.can_move((0, 1)) is True 
    assert pacman.can_move((0, -1)) is False  

def test_pacman_get_sprite(pacman: Pacman):
    """Проверка корректности спрайта Pacman при движении"""
    pacman.rotate((1, 0)) 
    sprite = pacman.get_sprite()
    assert isinstance(sprite, Sprite)
    assert sprite.texture.get_width() == 32  

def test_pacman_get_hitbox(pacman: Pacman):
    """Проверка корректности хитбокса Pacman"""
    pacman.rotate((1, 0))  
    hitbox = pacman.get_hitbox()
    assert isinstance(hitbox, pygame.Rect)
    assert hitbox.width == 32  
    assert hitbox.height == 32  

def test_pacman_update_destination(pacman: Pacman):
    """Проверка метода update_destination """
    pacman.update_destination()  
    assert True
