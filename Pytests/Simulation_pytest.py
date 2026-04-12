import pytest
import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Python.simulation import Simulation

@pytest.fixture
def sim():
    pygame.init()
    sim = Simulation(1200, 800, floors=6)
    yield sim
    pygame.quit()
    
def test_add_normal_lift_increases_count(sim):
    start_count = len(sim.lifts)
    sim.add_lift("normal")
    assert len(sim.lifts) == start_count + 1
    assert sim.lifts[-1]["type"] == "normal"


def test_add_fast_lift_increases_count(sim):
    start_count = len(sim.lifts)
    sim.add_lift("fast")
    assert len(sim.lifts) == start_count + 1
    assert sim.lifts[-1]["type"] == "fast"


def test_invalid_lift_type_does_not_add_lift(sim):
    start_count = len(sim.lifts)
    sim.add_lift("invalid")
    assert len(sim.lifts) == start_count


def test_lift_count_has_maximum_of_eight(sim):
    for _ in range(20):
        sim.add_lift("fast")
    assert len(sim.lifts) == 8


def test_remove_last_lift_removes_one_lift(sim):
    sim.add_lift("fast")
    start_count = len(sim.lifts)
    sim.remove_last_lift()
    assert len(sim.lifts) == start_count - 1


def test_remove_last_lift_does_not_go_below_one(sim):
    sim.remove_last_lift()
    assert len(sim.lifts) == 1


def test_set_floors_updates_floor_count_and_lift_height(sim):
    sim.set_floors(8)
    assert sim.floors == 8
    assert sim.lift_h == pytest.approx(sim.building_height / 8, rel=1e-6)


def test_set_open_time_updates_opening_time(sim):
    sim.set_open_time(9, 30)
    assert sim.open_time_minutes == 9 * 60 + 30


def test_set_close_time_updates_closing_time(sim):
    sim.set_close_time(19, 15)
    assert sim.close_time_minutes == 19 * 60 + 15


def test_open_time_cannot_be_after_close_time(sim):
    sim.set_close_time(10, 0)
    sim.set_open_time(11, 0)
    assert sim.open_time_minutes == sim.close_time_minutes - 1


def test_close_time_cannot_be_before_open_time(sim):
    sim.set_open_time(9, 0)
    sim.set_close_time(8, 0)
    assert sim.close_time_minutes == sim.open_time_minutes + 1


def test_restart_day_resets_time_to_open_time(sim):
    sim.set_open_time(10, 0)
    sim.time_minutes = 14 * 60
    sim.restart_day()
    assert sim.time_minutes == 10 * 60


def test_restart_day_clears_people(sim):
    sim.people.append({"id": 1, "state": "WAITING", "x": 0, "y": 0, "floor": 0})
    sim.restart_day()
    assert sim.people == []


def test_day_finished_becomes_true_at_close_time(sim):
    sim.time_minutes = sim.close_time_minutes - 1
    sim.update(1.0)
    assert sim.day_finished is True
    assert sim.time_minutes == sim.close_time_minutes


def test_get_time_string_formats_correctly(sim):
    sim.time_minutes = 8 * 60 + 5
    assert sim.get_time_string() == "08:05"


def test_get_lift_destinations_counts_boarding_and_in_lift(sim):
    lift_id = sim.lifts[0]["id"]
    sim.people = [
        {"elevator_id": lift_id, "state": "BOARDING", "dest": 3},
        {"elevator_id": lift_id, "state": "IN_LIFT", "dest": 3},
        {"elevator_id": lift_id, "state": "IN_LIFT", "dest": 5},
        {"elevator_id": 999, "state": "IN_LIFT", "dest": 7},
    ]
    assert sim.get_lift_destinations(lift_id) == {3: 2, 5: 1}
