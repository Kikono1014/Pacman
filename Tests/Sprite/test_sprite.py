import sys
import types
import pytest

class DummySurface:
    def __init__(self):
        self.subsurfaces = []
    def subsurface(self, area):
        self.subsurfaces.append(area)
        return f"subsurface_of_{area}"

class DummyRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def __repr__(self):
        return f"Rect({self.x},{self.y},{self.w},{self.h})"

class DummyTransformModule:
    def __init__(self):
        self.calls = []
    def scale(self, texture, size):
        self.calls.append((texture, size))
        return f"scaled_{texture}_{size}"

@pytest.fixture(autouse=True)
def fake_pygame(monkeypatch):
    fake_pg = types.SimpleNamespace()
    fake_pg.Surface = DummySurface
    fake_pg.Rect = DummyRect
    fake_pg.transform = DummyTransformModule()
    
    monkeypatch.setitem(sys.modules, 'pygame', fake_pg)
    import sprite
    monkeypatch.setattr(sprite, 'pygame', fake_pg)
    return fake_pg

@pytest.fixture
def dummy_surface():
    return DummySurface()

@pytest.fixture
def dummy_rect():
    return DummyRect(5, 10, 20, 30)

from sprite import Sprite

def test_init_creates_texture_and_resets_area(dummy_surface, dummy_rect):
    spr = Sprite(dummy_surface, dummy_rect)
    assert dummy_rect in dummy_surface.subsurfaces
    assert dummy_rect.x == 0
    assert dummy_rect.y == 0
    assert spr.area is dummy_rect

@pytest.mark.parametrize('orig_w, orig_h, scale_factor', [
    (3, 4, 1),
    (5, 6, 2),
    (1, 2, 5),
])
def test_scale_updates_area_and_texture(fake_pygame, dummy_surface, dummy_rect, orig_w, orig_h, scale_factor):
    spr = Sprite(dummy_surface, dummy_rect)
    spr.area.w = orig_w
    spr.area.h = orig_h
    spr.texture = 'orig_tex'
    fake_pygame.transform.calls.clear()

    result = spr.scale(scale_factor)

    assert spr.area.w == orig_w * scale_factor
    assert spr.area.h == orig_h * scale_factor

    expected_size = (orig_w * scale_factor, orig_h * scale_factor)
    assert fake_pygame.transform.calls == [('orig_tex', expected_size)]

    assert spr.texture == f"scaled_orig_tex_{expected_size}"

    assert result is spr
