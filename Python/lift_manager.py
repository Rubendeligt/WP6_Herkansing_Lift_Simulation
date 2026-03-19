from Python.Lift import update_lift


class LiftManager:
    def update_lifts(self, lifts: list, people: list, dt: float, floors: int) -> None:
        for lift in lifts:
            lift_x_for_people = lift["shaft_x"] + lift["lift_w"] / 2
            lift["people_x"] = int(lift_x_for_people)

            lift_blocked = self._is_lift_blocked(lift, people, lift_x_for_people)

            if not lift_blocked:
                lift["floor_pos"], lift["dir"] = update_lift(
                    lift["floor_pos"],
                    lift["dir"],
                    lift["speed"],
                    dt,
                    floors
                )

            lift_floor_int = int(round(lift["floor_pos"]))
            lift["floor"] = lift_floor_int
            lift["ready"] = abs(lift["floor_pos"] - lift_floor_int) < 0.03

    def _is_lift_blocked(self, lift: dict, people: list, lift_x_for_people: float) -> bool:
        boarding_block = any(
            p["state"] == "BOARDING" and p.get("elevator_id") == lift["id"]
            for p in people
        )

        exiting_block = any(
            p["state"] == "EXITING"
            and p.get("elevator_id") == lift["id"]
            and abs(p["x"] - lift_x_for_people) < 40
            for p in people
        )

        return boarding_block or exiting_block