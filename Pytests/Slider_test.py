import pygame
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Python.Information import InformationPanel



@pytest.fixture
def panel():
    pygame.init()
    return InformationPanel(1200, 800)


def test_panel_starts_closed(panel):
    assert panel.open is False
    assert panel.x == 1200
    assert panel.target_x == 1200


def test_toggle_opens_panel(panel):
    panel.toggle()

    assert panel.open is True
    assert panel.target_x == 1200 - panel.width


def test_toggle_closes_panel(panel):
    panel.toggle()
    panel.toggle()

    assert panel.open is False
    assert panel.target_x == 1200


def test_update_moves_panel(panel):
    panel.toggle()
    start_x = panel.x

    panel.update(0.1)

    assert panel.x < start_x


def test_button_click_opens_panel(panel):
    button_rect = panel.get_button_rect()

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {"pos": button_rect.center, "button": 1}
    )

    panel.handle_event(event)

    assert panel.open is True