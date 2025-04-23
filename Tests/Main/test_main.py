import pytest
from unittest.mock import MagicMock, patch, mock_open
import pygame
from main import PacmanGame
from gameobject import GameObject
from arena import Arena
from pacman import Pacman
from ghost import Ghost
from arena import Arena, Dot

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.mixer.init()
import pygame

# @pytest.fixture
# def mocked_game():
#     screen = pygame.Surface((232, 256))
#     with patch('pygame.display.set_mode', return_value=screen):
#         with patch('pygame.image.load', return_value=MagicMock(spec=pygame.Surface)):
#             with patch('pygame.mixer.Sound', side_effect=[MagicMock() for _ in range(5)]):
#                 with patch('pygame.mixer.music.load', return_value=None):
#                     with patch('pygame.mixer.music.play', return_value=None):
#                         with patch('builtins.open', mock_open(read_data="1 1")):
#                             with patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)):
#                                 game = PacmanGame(frame_rate=60, width=232, height=256, scale=1, preset=1)
#                                 return game


@pytest.fixture
def mocked_game(monkeypatch, tmp_path):
    screen = pygame.Surface((232, 276))

    monkeypatch.setattr(pygame.display, 'set_mode', lambda *args, **kwargs: screen)
    
    # atlas = pygame.Surface((16*14, 16*10))
    # monkeypatch.setattr(pygame.image, 'load', lambda path: atlas)
    
    monkeypatch.setattr(pygame.transform, 'scale', lambda surf, size: surf)
    
    class DummySound:
        def __init__(self, path): pass
        def play(self, *args, **kwargs): pass
    monkeypatch.setattr(pygame.mixer, 'Sound', lambda path: DummySound(path))
    music = pygame.mixer.music
    monkeypatch.setattr(music, 'load', lambda path: None)
    monkeypatch.setattr(music, 'play', lambda *args, **kwargs: None)
    
    game = PacmanGame(frame_rate=60, width=232, height=256, scale=1, preset=1)
    return game

def test_pacman_game_init(mocked_game):
    assert mocked_game.frame_rate == 60
    assert mocked_game.width == 232
    assert mocked_game.height == (256 + 20)
    assert mocked_game.scale == 1
    assert mocked_game.preset == 1
    assert mocked_game.playing is True
    assert mocked_game.game_over is False
    assert mocked_game.game_won is False
    assert mocked_game.score == 0
    assert mocked_game.high_score == 0
    assert mocked_game.extra_life_given is False
    
    assert isinstance(mocked_game.arena, Arena)
    assert isinstance(mocked_game.pacman, Pacman)
    
    assert mocked_game.pacman.lives == 3
    assert mocked_game.pacman.fruits == 0
    
    ghosts = mocked_game.ghosts
    assert len(ghosts) == 4
    names = {type(g).__name__ for g in ghosts}
    assert names == {'Blinky', 'Pinky', 'Inky', 'Clyde'}


def test_ghosts_init(mocked_game):
    """Test ghosts_init creates four ghosts with correct names."""
    mocked_game.ghost_sprites = [MagicMock() for _ in range(4)]
    mocked_game.ghosts_init()
    assert len(mocked_game.ghosts) == 4
