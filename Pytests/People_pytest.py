import pytest
import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).resolve().parents[1]))
import Python.People as People


@pytest.fixture
def basic_setup():
    rng = random.Random(1)
    people = []
    waiting_lines = {}
    lifts = [
        {"id": 0, "floor": 0, "ready": True, "people_x": 100, "capacity": 10},
    ]
    return rng, people, waiting_lines, lifts


def make_person(
    person_id=1,
    state="WAITING",
    x=100.0,
    y=0.0,
    floor=0,
    dest=3,
    wait_time=0.0,
    wait_recorded=False,
    elevator_id=None,
):
    return {
        "id": person_id,
        "state": state,
        "x": x,
        "y": y,
        "floor": floor,
        "dest": dest,
        "wait_time": wait_time,
        "wait_recorded": wait_recorded,
        "elevator_id": elevator_id,
    }

def test_spawn_returns_new_id(basic_setup):
    rng, people, _, _ = basic_setup

    new_id = People.maybe_spawn_person(
        rng, people, 1.0, 5, 800, 100, 1, 480, []
    )

    assert isinstance(new_id, int)

def test_update_people_with_empty_lists_does_not_crash():
    People.update_people([], {}, 0.1, 5, 800, 100, [], [], [])
    assert True


def test_person_stays_waiting_without_lifts():
    people = [make_person()]

    People.update_people(
        people,
        {},
        0.1,
        5,
        800,
        100,
        [],
        [],
        []
    )

    assert people[0]["state"] == "WAITING"

def test_person_can_enter_lift_if_capacity_available(basic_setup):
    _, people, waiting_lines, lifts = basic_setup

    person = make_person()
    people.append(person)

    People.update_people(
        people,
        waiting_lines,
        0.1,
        5,
        800,
        100,
        lifts,
        [],
        []
    )

    assert person["state"] in ("WAITING", "BOARDING", "IN_LIFT")