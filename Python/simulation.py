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

        self.normal_speed = LIFT_SPEED_FLOORS_PER_SEC
        self.fast_speed = LIFT_SPEED_FLOORS_PER_SEC * 2.2

        self.shaft_w = 70
        self.lift_w = int(self.shaft_w * 0.85)
        self.lift_h = self.building_height / self.floors
        self.shaft_gap = 20
        self.start_x = LEFT_MARGIN + 20

        self.lifts = []
        self.next_lift_id = 0
        self.add_lift("normal")
        self.add_lift("normal")
        for _ in range(6):
            self.add_lift("fast")

        self.rng = random.Random(7)
        self.people = []
        self.waiting_lines = {}
        self.next_person_id = 1
        self.completed_wait_times = []
        self.recent_wait_times = []
        self.wait_time_timer = 0.0
        self.displayed_average_wait_time = 0.0
        self.wait_time_history = []
        self.people_history = []

        self.time_minutes = 7 * 60
        self.time_speed = 5
        self.last_logged_hour = int(self.time_minutes // 60)

        self.maybe_spawn_person = PeopleModule.maybe_spawn_person
        self.update_people = PeopleModule.update_people

    def _recalculate_lift_layout(self) -> None:
        self.total_lifts = len(self.lifts)
        self.normal_lifts = sum(1 for lift in self.lifts if lift["type"] == "normal")
        self.fast_lifts = sum(1 for lift in self.lifts if lift["type"] == "fast")

        self.shaft_positions = [
            self.start_x + i * (self.shaft_w + self.shaft_gap)
            for i in range(self.total_lifts)
        ]

        for i, lift in enumerate(self.lifts):
            lift["shaft_x"] = self.shaft_positions[i]
            lift["shaft_w"] = self.shaft_w
            lift["lift_w"] = self.lift_w
            lift["lift_h"] = self.lift_h
            lift["people_x"] = int(self.shaft_positions[i] + self.shaft_w / 2)

        if self.total_lifts > 0:
            self.right_margin = self.shaft_positions[-1] + self.shaft_w + 40
        else:
            self.right_margin = self.start_x + 40

        self.rest_x = self.right_margin + 120
        self.call_x = self.right_margin + 25

    def add_lift(self, lift_type: str) -> None:
        if lift_type not in ("normal", "fast"):
            return

        speed = self.normal_speed if lift_type == "normal" else self.fast_speed

        new_lift = {
            "id": self.next_lift_id,
            "type": lift_type,
            "shaft_x": 0,
            "shaft_w": self.shaft_w,
            "lift_w": self.lift_w,
            "lift_h": self.lift_h,
            "floor_pos": float(min(self.floors - 1, len(self.lifts))),
            "dir": 1 if len(self.lifts) % 2 == 0 else -1,
            "speed": speed,
            "floor": min(self.floors - 1, len(self.lifts)),
            "ready": True,
            "people_x": 0,
        }

        self.next_lift_id += 1
        self.lifts.append(new_lift)
        self._recalculate_lift_layout()

    def remove_last_lift(self) -> None:
        if len(self.lifts) <= 1:
            return

        removed_lift = self.lifts.pop()
        for person in self.people:
            if person.get("elevator_id") == removed_lift["id"]:
                person["elevator_id"] = None
                if person["state"] == "IN_LIFT":
                    person["state"] = "WAITING"
                elif person["state"] in ("BOARDING", "EXITING"):
                    person["state"] = "WAITING"

        self._recalculate_lift_layout()

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

        self._recalculate_lift_layout()
    def update(self, dt: float) -> None:
        self.time_minutes += dt * self.time_speed
        if self.time_minutes > 21 * 60:
            self.time_minutes = 21 * 60
           
        self.wait_time_timer += dt

        if self.wait_time_timer >= 10.0:
            if self.recent_wait_times:
                self.displayed_average_wait_time = (
                    sum(self.recent_wait_times) / len(self.recent_wait_times)
                )
            else:
                self.displayed_average_wait_time = 0.0

            current_hour = int(self.time_minutes // 60)

            if current_hour != self.last_logged_hour:
                self.wait_time_history.append(
                    (self.time_minutes, self.displayed_average_wait_time)
                )
                self.people_history.append(
                    (self.time_minutes, len(self.people))
                )
                self.last_logged_hour = current_hour

            self.recent_wait_times.clear()
            self.wait_time_timer = 0.0

        self.next_person_id = self.maybe_spawn_person(
            self.rng,
            self.people,
            dt,
            self.floors,
            self.height,
            self.rest_x,
            self.next_person_id,
            self.time_minutes
        )

        for lift in self.lifts:
            lift_x_for_people = lift["shaft_x"] + lift["shaft_w"] / 2
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
    
    def get_time_string(self) -> str:
        total_minutes = int(self.time_minutes)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    
    def get_wait_time_history(self):
        return self.wait_time_history

    def get_people_history(self):
        return self.people_history