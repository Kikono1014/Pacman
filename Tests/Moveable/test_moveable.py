import pytest
from unittest.mock import Mock
import pygame
from moveable import Moveable

class TestMoveable(Moveable):
    def __init__(self, sprites, position, direction, speed, arena=None):
        super().__init__(sprites, position, direction, speed)
        self.arena = arena

@pytest.fixture
def test_sprite():
    sprite = Mock()
    sprite.area = pygame.Rect(0, 0, 32, 32)
    return sprite

@pytest.fixture
def test_arena():
    # 10x10 map for wrapping tests
    return type('TestArena', (), {'map': [[0] * 10 for _ in range(10)]})()

def test_init(test_sprite):
    position = (1, 2)
    direction = (1, 0)
    speed = 1.5
    moveable = TestMoveable([test_sprite], position, direction, speed, arena=None)
    assert moveable.position == position
    assert moveable.direction == direction
    assert moveable.speed == speed
    assert moveable.arena is None

@pytest.mark.parametrize("initial_position, direction, speed, expected_position", [
    ((0, 0), (1, 0), 0.5, (0.5, 0)),      # Move right
    ((1, 1), (0, 1), 1.0, (1, 2)),        # Move down
])
def test_move_without_arena(test_sprite, initial_position, direction, speed, expected_position):
    moveable = TestMoveable([test_sprite], initial_position, direction, speed, arena=None)
    moveable.move()
    assert moveable.position == expected_position

@pytest.mark.parametrize("initial_position, direction, speed, expected_position", [
    ((9.5, 0), (1, 0), 1.0, (0.5, 0)),    # Wrap right
    ((0, 0), (-1, 0), 1.0, (9.0, 0)),     # Wrap left
    ((0, 9.5), (0, 1), 1.0, (0, 0.5)),    # Wrap down
    ((0, 0), (0, -1), 1.0, (0, 9.0)),     # Wrap up
    ((5, 5), (1, 0), 0.5, (5.5, 5)),    # No wrap
])
def test_move_with_arena(test_sprite, test_arena, initial_position, direction, speed, expected_position):
    moveable = TestMoveable([test_sprite], initial_position, direction, speed, arena=test_arena)
    moveable.move()
    assert moveable.position[0] == pytest.approx(expected_position[0])
    assert moveable.position[1] == pytest.approx(expected_position[1])

# Test rotate method
@pytest.mark.parametrize("initial_direction, new_direction", [
    ((1, 0), (0, 1)),   # Right to down
    ((0, 1), (-1, 0)),  # Down to left
    ((-1, 0), (0, -1)), # Left to up
    ((0, -1), (1, 0)),  # Up to right
])
def test_rotate(test_sprite, initial_direction, new_direction):
    moveable = TestMoveable([test_sprite], (0, 0), initial_direction, 1.0, arena=None)
    moveable.rotate(new_direction)
    assert moveable.direction == new_direction

@pytest.mark.parametrize("position, sprite_area, expected_hitbox", [
    ((0, 0), pygame.Rect(0, 0, 32, 32), pygame.Rect(0, 0, 32, 32)),
    ((1, 0), pygame.Rect(0, 0, 32, 32), pygame.Rect(16, 0, 32, 32)),
    ((0, 1), pygame.Rect(0, 0, 32, 32), pygame.Rect(0, 16, 32, 32)),
    ((0.5, 0.5), pygame.Rect(0, 0, 32, 32), pygame.Rect(8, 8, 32, 32)),
    ((2, 3), pygame.Rect(0, 0, 64, 64), pygame.Rect(64, 96, 64, 64)),
])
def test_get_hitbox(position, sprite_area, expected_hitbox):
    sprite = Mock()
    sprite.area = sprite_area
    moveable = TestMoveable([sprite], position, (1, 0), 1.0, arena=None)
    hitbox = moveable.get_hitbox()
    assert hitbox == expected_hitbox