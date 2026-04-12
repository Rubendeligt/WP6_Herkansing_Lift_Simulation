import pygame
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from Python.Setting_sidebar import SettingSidebar


@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def sidebar():
    return SettingSidebar(1600, 900)


def test_setting_sidebar_starts_closed(sidebar):
    assert sidebar.is_open is False
    assert sidebar.x == sidebar.closed_x


def test_tab_click_opens_sidebar(sidebar):
    tab_rect = sidebar.get_tab_rect()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {"button": 1, "pos": tab_rect.center},
    )
    sidebar.handle_event(event)
    assert sidebar.is_open is True


def test_update_moves_sidebar_when_open(sidebar):
    sidebar.is_open = True
    start_x = sidebar.x
    sidebar.update(0.1)
    assert sidebar.x < start_x

def test_get_button_rects_returns_expected_number(sidebar):
    rects = sidebar.get_button_rects()
    assert len(rects) >= 5
    assert all(isinstance(rect, pygame.Rect) for rect in rects)
