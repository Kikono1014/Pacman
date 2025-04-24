import pytest
from unittest.mock import patch, mock_open, MagicMock
from arena import Arena, Dot
from sprite import Sprite
import pygame

@pytest.fixture
def mock_arena():
    # Mock file data for a 3x3 map
    mock_size = mock_open(read_data="3 3\n")
    mock_walls = mock_open(read_data="0 0\n2 2\n")
    mock_pellets = mock_open(read_data="1 1\n")
    mock_pacman_start = mock_open(read_data="1 0\n")
    mock_ghost_start = mock_open(read_data="1 2\n")
    
    # Mock pygame.image.load to return a MagicMock with subsurface returning another MagicMock
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.subsurface.return_value = MagicMock(spec=pygame.Surface)
    
    # Patch builtins.open, pygame.image.load, and pygame.transform.scale
    with patch('builtins.open', side_effect=[
        mock_size(), mock_walls(), mock_pellets(), mock_pacman_start(), mock_ghost_start()
    ]):
        with patch('pygame.image.load', return_value=mock_surface):
            with patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)):
                # Mock Sprite
                mock_sprite = MagicMock()
                mock_sprite.texture = MagicMock(spec=pygame.Surface)
                mock_sprite.area = pygame.Rect(0, 0, 16, 16)
                dot_sprites = [mock_sprite] * 5  # 5 sprites: normal, empty, pellet, 2 fruits
                
                # Create Arena
                area = pygame.Rect(0, 0, 48, 48)  # 3x3 grid with each cell 16x16
                scale = 1.0
                preset = 1
                arena = Arena(area, scale, dot_sprites, preset)
                yield arena

def test_init(mock_arena):
    """Test that __init__ correctly initializes the Arena and calls build."""
    arena = mock_arena
    assert arena.area == pygame.Rect(0, 0, 48, 48)
    assert arena.scale == 1.0
    assert arena.preset == 1
    assert len(arena.dot_sprites) == 5
    assert isinstance(arena.background, Sprite)
    assert arena.pacman_start == (1, 0)
    assert arena.ghost_start == (1, 2)
    assert len(arena.map) == 3
    assert len(arena.map[0]) == 3

def test_build(mock_arena):
    """Test the build method sets up the map and background correctly."""
    arena = mock_arena
    # Check map size
    assert len(arena.map) == 3  # height
    assert len(arena.map[0]) == 3  # width
    
    # Check walls
    assert arena.map[0][0] == Dot.WALL
    assert arena.map[2][2] == Dot.WALL
    
    # Check pellets
    assert arena.map[1][1] == Dot.PELLET
    
    # Check normal dots
    assert arena.map[0][1] == Dot.NORMAL
    assert arena.map[0][2] == Dot.NORMAL
    assert arena.map[1][0] == Dot.NORMAL
    assert arena.map[1][2] == Dot.NORMAL
    assert arena.map[2][0] == Dot.NORMAL
    assert arena.map[2][1] == Dot.NORMAL
    
    # Check pacman_start and ghost_start
    assert arena.pacman_start == (1, 0)
    assert arena.ghost_start == (1, 2)
    
    # Check if blit was called for each non-wall cell (9 cells - 2 walls = 7 blits)
    assert arena.background.texture.blit.call_count == 7

@pytest.mark.parametrize("position, initial_dot, should_remove, expected_size_factor", [
    ((1, 1), Dot.PELLET, True, (0.5, 0.5)),         # Remove pellet
    ((0, 1), Dot.NORMAL, True, (0.5, 0.5)),         # Remove normal dot
    ((2, 1), Dot.FRUIT, True, (1 - 1/8, 1 - 1/8)),  # Remove fruit
    ((0, 0), Dot.WALL, False, None),                # Wall, no removal
    ((3, 3), None, False, None),                    # Out of bounds
])
def test_remove_dot(mock_arena, position, initial_dot, should_remove, expected_size_factor):
    """Test remove_dot updates the map and blits correctly."""
    arena = mock_arena
    x, y = position
    if 0 <= y < len(arena.map) and 0 <= x < len(arena.map[0]):
        arena.map[y][x] = initial_dot
    with patch('pygame.Surface') as mock_surface:
        arena.background.texture.blit.reset_mock()
        arena.remove_dot(position)
        if should_remove:
            assert arena.map[y][x] == Dot.EMPTY
            w = arena.dot_sprites[1].area.w
            h = arena.dot_sprites[1].area.h
            expected_size = (w * expected_size_factor[0], h * expected_size_factor[1])
            mock_surface.assert_called_with(expected_size)
            assert arena.background.texture.blit.called
        else:
            if 0 <= y < len(arena.map) and 0 <= x < len(arena.map[0]):
                assert arena.map[y][x] == initial_dot
            mock_surface.assert_not_called()
            assert not arena.background.texture.blit.called

@pytest.mark.parametrize("dot_type, expected_positions", [
    (Dot.NORMAL, [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]),
    (Dot.PELLET, [(1, 1)]),
    (Dot.WALL, [(0, 0), (2, 2)]),
    (Dot.EMPTY, []),
    (Dot.FRUIT, []),
])
def test_get_dots(mock_arena, dot_type, expected_positions):
    """Test get_dots returns correct positions for given dot type."""
    arena = mock_arena
    dots = arena.get_dots(dot_type)
    assert sorted(dots) == sorted(expected_positions)

def test_add_fruit(mock_arena):
    """Test add_fruit adds a fruit to an empty spot with correct sprite."""
    arena = mock_arena
    # Create an empty spot
    arena.remove_dot((0, 1))  # Originally NORMAL
    assert arena.map[1][0] == Dot.EMPTY
    
    with patch('random.choice', return_value=(0, 1)):
        arena.background.texture.blit.reset_mock()
        arena.add_fruit(pacman_fruits=0)
        assert arena.map[1][0] == Dot.FRUIT
        # Check that the correct fruit sprite (index 3) is blitted
        assert arena.background.texture.blit.call_args[0][0] == arena.dot_sprites[3].texture

def test_add_fruit_no_empty(mock_arena):
    """Test add_fruit does nothing when there are no empty spots."""
    arena = mock_arena
    with patch('random.choice') as mock_choice:
        arena.background.texture.blit.reset_mock()
        arena.add_fruit(pacman_fruits=0)
        mock_choice.assert_not_called()
        assert all(dot != Dot.FRUIT for row in arena.map for dot in row)
        assert not arena.background.texture.blit.called

@pytest.mark.parametrize("position, expected_hitbox", [
    ((0, 0), pygame.Rect(0, 0, 16, 16)),
    ((1, 0), pygame.Rect(8, 0, 16, 16)),
    ((0, 1), pygame.Rect(0, 8, 16, 16)),
    ((1, 1), pygame.Rect(8, 8, 16, 16)),
])
def test_get_dot_hitbox(mock_arena, position, expected_hitbox):
    """Test get_dot_hitbox returns correct Rect for a position."""
    arena = mock_arena
    hitbox = arena.get_dot_hitbox(position)
    assert hitbox == expected_hitbox