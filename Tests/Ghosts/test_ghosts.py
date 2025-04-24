import sys
import os
# Додаємо корінь проєкту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
import pygame
from unittest.mock import Mock, patch
from ghost import Ghost
from ghosts import Blinky, Pinky, Inky, Clyde
from pacman import Pacman
from arena import Arena, Dot
from sprite import Sprite

# Фікстура для ініціалізації pygame
@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# Фікстура для створення тестової арени
@pytest.fixture
def arena():
    dot_sprites = [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(5)]
    arena = Arena(pygame.Rect(0, 0, 232, 256), scale=2.0, dot_sprites=dot_sprites, preset=1)
    # Мапа: стіна ліворуч (2,1), решта вільно
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

# Фікстура для створення Пакмена
@pytest.fixture
def pacman(arena):
    sprites = [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(3)]
    pacman = Pacman(sprites, arena.pacman_start, (1, 0), 0.108, arena)
    pacman.game = Mock()
    return pacman

# Фікстура для створення загального привида
@pytest.fixture
def ghost(arena, pacman):
    sprites = [
        [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(2)],
        [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(2)],
        [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(2)],
        [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(2)],
        [Sprite(pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)) for _ in range(4)]
    ]
    ghost = Ghost(sprites, arena.ghost_start, (1, 0), 0.09, arena, pacman)
    ghost.game = Mock()
    return ghost

# Тести для класу Ghost
@pytest.mark.initialization
def test_ghost_initialization(ghost, arena, pacman):
    assert ghost.position == arena.ghost_start
    assert ghost.direction == (1, 0)
    assert ghost.speed == 0.09
    assert ghost.arena == arena
    assert ghost.pacman == pacman
    assert ghost.mode == "scatter"
    assert len(ghost.mode_schedule) == 8

@pytest.mark.movement
@pytest.mark.parametrize("direction, expected", [
    ((1, 0), True),   # Право - вільно
    ((0, 1), True),   # Вниз - вільно
    ((0, -1), True),  # Вгору - вільно
    ((-1, 0), False), # Ліво - стіна
])
def test_ghost_can_move(ghost, direction, expected):
    ghost.position = (2, 2)  # Центр мапи
    assert ghost.can_move(direction) == expected

@pytest.mark.movement
def test_ghost_move_inactive(ghost):
    ghost.is_active = False
    ghost.respawn_timer = 120
    original_position = ghost.position
    ghost.move(ghost.arena.map)
    assert ghost.position == original_position
    assert ghost.respawn_timer == 119

@pytest.mark.movement
def test_ghost_move_respawn(ghost):
    ghost.is_active = False
    ghost.respawn_timer = 1
    ghost.position = (0, 0)
    ghost.move(ghost.arena.map)
    assert ghost.position == ghost.arena.ghost_start
    assert ghost.is_active
    assert ghost.mode_index == 0
    assert ghost.mode_timer == 0

@pytest.mark.mode
def test_ghost_mode_schedule(ghost):
    ghost.mode_timer = 420
    ghost.move(ghost.arena.map)
    assert ghost.mode == "chase"
    assert ghost.mode_index == 1
    assert ghost.mode_timer == 0

@pytest.mark.mode
def test_ghost_set_frightened(ghost):
    ghost.set_frightened()
    assert ghost.mode == "frightened"
    assert ghost.frightened_timer == 420
    assert ghost.current_frame == 0

@pytest.mark.collision
def test_ghost_check_collision(ghost, pacman):
    ghost.position = pacman.position
    assert ghost.check_collision(pacman)

@pytest.mark.collision
def test_ghost_no_collision(ghost, pacman):
    ghost.position = (0, 0)
    pacman.position = (4, 4)
    assert not ghost.check_collision(pacman)

@pytest.mark.sprite
@patch("pygame.image.load")
def test_ghost_get_sprite_normal(mock_load, ghost):
    mock_load.return_value = pygame.Surface((256, 256))
    ghost.mode = "chase"
    ghost.direction = (1, 0)
    sprite = ghost.get_sprite()
    assert isinstance(sprite, Sprite)
    assert sprite.area.w == 16

@pytest.mark.sprite
@patch("pygame.image.load")
def test_ghost_get_sprite_frightened(mock_load, ghost):
    mock_load.return_value = pygame.Surface((256, 256))
    ghost.set_frightened()
    ghost.frightened_timer = 421
    sprite = ghost.get_sprite()
    assert isinstance(sprite, Sprite)
    sprite = ghost.get_sprite()
    assert isinstance(sprite, Sprite)

@pytest.mark.sprite
@patch("pygame.image.load")
def test_ghost_get_sprite_frightened_flash(mock_load, ghost):
    mock_load.return_value = pygame.Surface((256, 256))
    ghost.set_frightened()
    ghost.frightened_timer = 119
    sprite = ghost.get_sprite()
    assert isinstance(sprite, Sprite)
    sprite = ghost.get_sprite()
    assert isinstance(sprite, Sprite)

# Тести для Blinky
@pytest.mark.initialization
@patch("pygame.image.load")
def test_blinky_initialization(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    blinky = Blinky(arena.ghost_start, (0, 1), 0.09, arena, pacman, 2.0)
    assert blinky.scatter_point == (len(arena.map[0]) - 1, 0)
    assert len(blinky.sprites) == 5
    assert len(blinky.sprites[0]) == 2

@pytest.mark.destination
@patch("pygame.image.load")
def test_blinky_update_destination_chase(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    blinky = Blinky(arena.ghost_start, (0, 1), 0.09, arena, pacman, 2.0)
    blinky.mode = "chase"
    pacman.position = (3, 3)
    blinky.update_destination()
    assert blinky.destination == (3, 3)

@pytest.mark.destination
@patch("pygame.image.load")
def test_blinky_update_destination_scatter(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    blinky = Blinky(arena.ghost_start, (0, 1), 0.09, arena, pacman, 2.0)
    blinky.mode = "scatter"
    blinky.update_destination()
    assert blinky.destination == (len(arena.map[0]) - 1, 0)

# Тести для Pinky
@pytest.mark.initialization
@patch("pygame.image.load")
def test_pinky_initialization(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    pinky = Pinky(arena.ghost_start, (0, -1), 0.09, arena, pacman, 2.0)
    assert pinky.scatter_point == (0, 0)
    assert len(pinky.sprites) == 5

@pytest.mark.destination
@patch("pygame.image.load")
def test_pinky_update_destination_chase(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    pinky = Pinky(arena.ghost_start, (0, -1), 0.09, arena, pacman, 2.0)
    pinky.mode = "chase"
    pacman.position = (2, 2)
    pacman.direction = (1, 0)
    pinky.update_destination()
    assert pinky.destination == (6, 2)

@pytest.mark.destination
@patch("pygame.image.load")
def test_pinky_update_destination_scatter(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    pinky = Pinky(arena.ghost_start, (0, -1), 0.09, arena, pacman, 2.0)
    pinky.mode = "scatter"
    pinky.update_destination()
    assert pinky.destination == (0, 0)

# Тести для Inky
@pytest.mark.initialization
@patch("pygame.image.load")
def test_inky_initialization(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    inky = Inky(arena.ghost_start, (-1, 0), 0.09, arena, pacman, 2.0)
    assert inky.scatter_point == (len(arena.map[0]) - 1, len(arena.map) - 1)

@pytest.mark.destination
@patch("pygame.image.load")
def test_inky_update_destination_chase(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    game = Mock()
    blinky = Blinky(arena.ghost_start, (0, 1), 0.09, arena, pacman, 2.0)
    inky = Inky(arena.ghost_start, (-1, 0), 0.09, arena, pacman, 2.0)
    inky.game = game
    game.ghosts = [blinky, inky]
    inky.mode = "chase"
    pacman.position = (2, 2)
    pacman.direction = (1, 0)
    blinky.position = (1, 1)
    inky.update_destination()
    assert inky.destination == (7, 3)  # Виправлено відповідно до логіки Inky

@pytest.mark.destination
@patch("pygame.image.load")
def test_inky_update_destination_scatter(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    inky = Inky(arena.ghost_start, (-1, 0), 0.09, arena, pacman, 2.0)
    inky.mode = "scatter"
    inky.update_destination()
    assert inky.destination == (len(arena.map[0]) - 1, len(arena.map) - 1)

# Тести для Clyde
@pytest.mark.initialization
@patch("pygame.image.load")
def test_clyde_initialization(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    clyde = Clyde(arena.ghost_start, (1, 0), 0.09, arena, pacman, 2.0)
    assert clyde.scatter_point == (0, len(arena.map) - 1)

@pytest.mark.destination
@patch("pygame.image.load")
def test_clyde_update_destination_chase_far(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    clyde = Clyde(arena.ghost_start, (1, 0), 0.09, arena, pacman, 2.0)
    clyde.mode = "chase"
    pacman.position = (10, 10)
    clyde.position = (2, 2)
    clyde.update_destination()
    assert clyde.destination == (10, 10)

@pytest.mark.destination
@patch("pygame.image.load")
def test_clyde_update_destination_chase_near(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    clyde = Clyde(arena.ghost_start, (1, 0), 0.09, arena, pacman, 2.0)
    clyde.mode = "chase"
    pacman.position = (3, 3)
    clyde.position = (2, 2)
    clyde.update_destination()
    assert clyde.destination == (0, len(arena.map) - 1)

@pytest.mark.destination
@patch("pygame.image.load")
def test_clyde_update_destination_scatter(mock_load, arena, pacman):
    mock_load.return_value = pygame.Surface((256, 256))
    clyde = Clyde(arena.ghost_start, (1, 0), 0.09, arena, pacman, 2.0)
    clyde.mode = "scatter"
    clyde.update_destination()
    assert clyde.destination == (0, len(arena.map) - 1)

# Додаткові тести
@pytest.mark.movement
def test_ghost_move_frightened(ghost, pacman):
    ghost.set_frightened()
    ghost.position = (2, 2)
    pacman.position = (4, 4)
    ghost.move(ghost.arena.map)
    assert ghost.speed == ghost.base_speed * 0.5
    assert ghost.frightened_timer == 419

@pytest.mark.movement
def test_ghost_move_wrapping(ghost):
    ghost.position = (5.0, 2)
    ghost.direction = (1, 0)
    ghost.move(ghost.arena.map)
    assert ghost.position[0] < 1

@pytest.mark.sprite
def test_ghost_animation_frame_update(ghost):
    initial_frame = ghost.current_frame
    ghost.get_sprite()
    assert ghost.current_frame > initial_frame

@pytest.mark.mode
@pytest.mark.parametrize("mode_index, expected_mode", [
    (0, "chase"),
    (1, "scatter"),
    (7, "scatter")
])
def test_ghost_mode_transition(ghost, mode_index, expected_mode):
    ghost.mode_index = mode_index
    ghost.mode_timer = ghost.mode_schedule[mode_index][0]
    ghost.move(ghost.arena.map)
    assert ghost.mode == expected_mode

@pytest.mark.movement
def test_ghost_valid_directions(ghost):
    ghost.position = (2, 2)
    ghost.direction = (1, 0)
    ghost.move(ghost.arena.map)
    assert ghost.direction in [(1, 0), (0, 1), (0, -1)]