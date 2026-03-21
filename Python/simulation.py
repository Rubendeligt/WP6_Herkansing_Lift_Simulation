import random
from Python.Variables import (
    LEFT_MARGIN,
    LIFT_SPEED_FLOORS_PER_SEC,
    TOP_MARGIN,
    BOTTOM_MARGIN,
)
import Python.People as PeopleModule
from Python.Lift import update_lift


class Simulation:
    def __init__(self, width: int, height: int, floors: int = 6):
        self.width = width
        self.height = height
        self.floors = floors

        self.building_height = self.height - TOP_MARGIN - BOTTOM_MARGIN

        self.total_lifts = 8
        self.normal_lifts = 2
        self.fast_lifts = 6

        self.normal_speed = LIFT_SPEED_FLOORS_PER_SEC
        self.fast_speed = LIFT_SPEED_FLOORS_PER_SEC * 2.2

        self.shaft_w = 45
        self.lift_w = self.shaft_w
        self.lift_h = self.building_height / self.floors
        self.shaft_gap = 10
        self.start_x = LEFT_MARGIN + 20

        self.shaft_positions = [
            self.start_x + i * (self.shaft_w + self.shaft_gap)
            for i in range(self.total_lifts)
        ]

        self.right_margin = self.shaft_positions[-1] + self.shaft_w + 40
        self.rest_x = self.right_margin + 120
        self.call_x = self.right_margin + 25

        self.lifts = self._create_lifts()

        self.rng = random.Random(7)
        self.people = []
        self.waiting_lines = {}
        self.next_person_id = 1
        self.completed_wait_times = []
        self.recent_wait_times = []
        self.wait_time_timer = 0.0
        self.displayed_average_wait_time = 0.0

        self.maybe_spawn_person = PeopleModule.maybe_spawn_person
        self.update_people = PeopleModule.update_people

    def _create_lifts(self) -> list[dict]:
        lifts = []

        for i in range(self.total_lifts):
            speed = self.normal_speed if i < self.normal_lifts else self.fast_speed
            start_floor = min(self.floors - 1, int(i * self.floors / self.total_lifts))
            start_dir = 1 if i % 2 == 0 else -1

            lifts.append({
                "id": i,
                "shaft_x": self.shaft_positions[i],
                "shaft_w": self.shaft_w,
                "lift_w": self.lift_w,
                "lift_h": self.lift_h,
                "floor_pos": float(start_floor),
                "dir": start_dir,
                "speed": speed,
                "floor": start_floor,
                "ready": True,
                "people_x": int(self.shaft_positions[i] + self.lift_w / 2)
            })

        return lifts

    def set_floors(self, floors: int) -> None:
        self.floors = floors
        self.waiting_lines.clear()

        self.building_height = self.height - TOP_MARGIN - BOTTOM_MARGIN
        self.lift_h = self.building_height / self.floors

        for lift in self.lifts:
            if lift["floor_pos"] > self.floors - 1:
                lift["floor_pos"] = float(self.floors - 1)

            lift["lift_h"] = self.lift_h
            lift["floor"] = int(round(lift["floor_pos"]))

    def update(self, dt: float) -> None:
        self.wait_time_timer += dt

        if self.wait_time_timer >= 10.0:
            if self.recent_wait_times:
                self.displayed_average_wait_time = (
                    sum(self.recent_wait_times) / len(self.recent_wait_times)
                )
            else:
                self.displayed_average_wait_time = 0.0

            self.recent_wait_times.clear()
            self.wait_time_timer = 0.0

        self.next_person_id = self.maybe_spawn_person(
            self.rng,
            self.people,
            dt,
            self.floors,
            self.height,
            self.rest_x,
            self.next_person_id
        )

        for lift in self.lifts:
            lift_x_for_people = lift["shaft_x"] + lift["lift_w"] / 2
            lift["people_x"] = int(lift_x_for_people)

            lift_blocked = any(
                p["state"] == "BOARDING" and p.get("elevator_id") == lift["id"]
                for p in self.people
            ) or any(
                p["state"] == "EXITING"
                and p.get("elevator_id") == lift["id"]
                and abs(p["x"] - lift_x_for_people) < 40
                for p in self.people
            )

            if not lift_blocked:
                lift["floor_pos"], lift["dir"] = update_lift(
                    lift["floor_pos"],
                    lift["dir"],
                    lift["speed"],
                    dt,
                    self.floors
                )

            lift_floor_int = int(round(lift["floor_pos"]))
            lift["floor"] = lift_floor_int
            lift["ready"] = abs(lift["floor_pos"] - lift_floor_int) < 0.03

        self.update_people(
            self.people,
            self.waiting_lines,
            dt,
            self.floors,
            self.height,
            self.call_x,
            self.lifts,
            self.completed_wait_times,
            self.recent_wait_times
        )

        self.people[:] = [
            p for p in self.people
            if not (p["state"] == "EXITING" and p["x"] > self.width + 50)
        ]

    def get_passenger_count(self, lift_id: int) -> int:
        return sum(
            1
            for p in self.people
            if p["state"] == "IN_LIFT" and p.get("elevator_id") == lift_id
        )
    
    def get_average_wait_time(self) -> float:
        return self.displayed_average_wait_time