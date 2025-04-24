# Tests/conftest.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pygame
from arena import Arena, Dot
from sprite import Sprite

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def arena():
    dot_sprites = [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(5)]
    arena = Arena(pygame.Rect(0, 0, 232, 256), scale=2.0, dot_sprites=dot_sprites, preset=1)
    arena.map = [
        [Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY],
        [Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY],
        [Dot.EMPTY, Dot.WALL, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY],
        [Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY],
        [Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY, Dot.EMPTY]
    ]
    arena.ghost_start = (2, 2)
    arena.pacman_start = (2, 2)
    return arena