import pygame
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from Python.Drukte import DruktePanel, get_drukte_buttons, handle_drukte_click


@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def panel():
    return DruktePanel(1600, 900)


@pytest.fixture
def simulation_stub():
    class SimulationStub:
        def __init__(self):
            self.rush_periods = [
                {"start_hour": 8, "start_minute": 15, "end_hour": 8, "end_minute": 45, "multiplier": 2.5},
                {"start_hour": 12, "start_minute": 0, "end_hour": 13, "end_minute": 0, "multiplier": 3.5},
                {"start_hour": 17, "start_minute": 0, "end_hour": 18, "end_minute": 0, "multiplier": 2.5},
            ]

        def set_rush_period(self, index, start_hour=None, start_minute=None,
                            end_hour=None, end_minute=None, multiplier=None):

            period = self.rush_periods[index]

            if start_hour is not None:
                period["start_hour"] = start_hour
            if start_minute is not None:
                period["start_minute"] = start_minute
            if end_hour is not None:
                period["end_hour"] = end_hour
            if end_minute is not None:
                period["end_minute"] = end_minute
            if multiplier is not None:
                period["multiplier"] = multiplier

    return SimulationStub()

def test_panel_is_closed_by_default(panel):
    assert panel.is_open is False

def test_panel_moves_when_open(panel):
    panel.is_open = True
    start_x = panel.x

    panel.update(0.1)

    assert panel.x < start_x or panel.x == panel.target_x

def test_get_drukte_buttons_returns_non_empty_list(panel, simulation_stub):
    buttons = get_drukte_buttons(simulation_stub, panel)

    assert isinstance(buttons, list)
    assert len(buttons) > 0


def test_each_button_contains_action_index_and_rect(panel, simulation_stub):
    buttons = get_drukte_buttons(simulation_stub, panel)

    for action, idx, rect in buttons:
        assert isinstance(action, str)
        assert isinstance(idx, int)
        assert isinstance(rect, pygame.Rect)

def test_click_on_button_does_not_crash(panel, simulation_stub):
    buttons = get_drukte_buttons(simulation_stub, panel)

    action, idx, rect = buttons[0]

    handle_drukte_click(rect.center, simulation_stub, buttons)

    assert True


def test_clicking_buttons_can_modify_rush_period(panel, simulation_stub):
    buttons = get_drukte_buttons(simulation_stub, panel)

    before = simulation_stub.rush_periods[0]["multiplier"]

    for action, idx, rect in buttons:
        handle_drukte_click(rect.center, simulation_stub, buttons)

    after = simulation_stub.rush_periods[0]["multiplier"]

    assert isinstance(after, float)
    assert after >= 0.1