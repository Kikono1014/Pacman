import pygame
import pytest
from unittest.mock import MagicMock
from gameobject import GameObject
from sprite import Sprite

pygame.init()

@pytest.fixture
def test_surface():
    return pygame.Surface((100, 100))

@pytest.fixture
def test_sprites(test_surface):
    rect1 = pygame.Rect(0, 0, 16, 16)
    rect2 = pygame.Rect(16, 0, 16, 16)
    return [Sprite(test_surface, rect1), Sprite(test_surface, rect2)]

@pytest.fixture
def test_position():
    return (10, 10)

def test_gameobject_init(test_sprites, test_position):
    gameobject = GameObject(test_sprites, test_position)
    assert gameobject.sprites == test_sprites
    assert gameobject.current == 0
    assert gameobject.position == test_position

def test_gameobject_get_hitbox(test_sprites, test_position):
    gameobject = GameObject(test_sprites, test_position)
    hitbox = gameobject.get_hitbox()
    expected_hitbox = pygame.Rect(
        test_position[0] * test_sprites[0].area.w / 2,
        test_position[1] * test_sprites[0].area.h / 2,
        test_sprites[0].area.w,
        test_sprites[0].area.h
    )
    assert hitbox == expected_hitbox


def test_gameobject_get_sprite(test_sprites, test_position):
    gameobject = GameObject(test_sprites, test_position)
    sprite = gameobject.get_sprite()
    assert sprite == test_sprites[0]


@pytest.mark.parametrize("sprite_id, expected_current", [
    (0, 0),
    (1, 1),
    (-1, -1),
])
def test_gameobject_change_sprite(test_sprites, test_position, sprite_id, expected_current):
    gameobject = GameObject(test_sprites, test_position)
    gameobject.change_sprite(sprite_id)
    assert gameobject.current == expected_current
