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