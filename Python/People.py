import random
import pygame
from Python.Variables import (
    TOP_MARGIN,
    BOTTOM_MARGIN,
    PERSON_RADIUS,
    PERSON_SPEED_PX_PER_SEC,
    SPAWN_CHANCE_PER_SEC,
    SPAWN_RECT_X,
    SPAWN_RECT_Y,
    SPAWN_RECT_W,
    SPAWN_RECT_H,
)


def floor_center_y(floor_index: int, floors: int, HEIGHT: int) -> float:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    floor_height = building_height / floors
    return TOP_MARGIN + (floors - 1 - floor_index) * floor_height + floor_height / 2


def maybe_spawn_person(
    rng: random.Random,
    people: list,
    dt: float,
    floors: int,
    HEIGHT: int,
    rest_x: int,
    next_person_id: int,
    time_minutes: float
) -> int:
    hours = int(time_minutes // 60)
    minutes = int(time_minutes % 60)

    spawn_rate = SPAWN_CHANCE_PER_SEC
    if (hours == 8 and minutes >= 15) or (hours == 8 and minutes < 45):
        spawn_rate *= 2.5
    elif hours == 12:
        spawn_rate *= 3.5
    elif hours == 17:
        spawn_rate *= 2.5

    elif hours >= 18:
        spawn_rate *= 0.25

    if rng.random() < spawn_rate * dt:
        start_floor = rng.randrange(0, floors)
        y = floor_center_y(start_floor, floors, HEIGHT)

        dest_floor = rng.randrange(0, floors)
        while dest_floor == start_floor and floors > 1:
            dest_floor = rng.randrange(0, floors)
        spawn_x = SPAWN_RECT_X

        people.append({
            "id": next_person_id,
            "floor": start_floor,
            "dest": dest_floor,
            "x": float(spawn_x),
            "y": float(y),
            "state": "WALKING",
            "elevator_id": None,
            "wait_time": 0.0,
            "wait_recorded": False
        })
        next_person_id += 1

    return next_person_id


def update_people(
    people: list,
    waiting_lines: dict,
    dt: float,
    floors: int,
    HEIGHT: int,
    call_x: int,
    lifts: list,
    completed_wait_times: list,
    recent_wait_times: list
) -> None:
    spacing = PERSON_RADIUS * 2 + 6
    waiting_lines.clear()
    exit_x = SPAWN_RECT_X

    ready_lifts_by_floor = {}
    for lift in lifts:
        if lift["ready"]:
            ready_lifts_by_floor.setdefault(lift["floor"], []).append(lift)

    for p in people:
        if p["floor"] > floors - 1:
            p["floor"] = floors - 1
        if p["floor"] < 0:
            p["floor"] = 0

        if p["state"] == "WALKING":
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

            if p["x"] > call_x:
                p["x"] -= PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] <= call_x:
                    p["x"] = float(call_x)
                    p["state"] = "WAITING"

        if p["state"] == "WAITING":
            p["wait_time"] += dt
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

            waiting_lines.setdefault(p["floor"], []).append(p["id"])
            idx = waiting_lines[p["floor"]].index(p["id"])
            p["x"] = float(call_x + idx * spacing)

            floor_lifts = ready_lifts_by_floor.get(p["floor"], [])
            if floor_lifts:
                chosen_lift = min(
                    floor_lifts,
                    key=lambda lift: abs(p["x"] - lift["people_x"])
                )
                p["state"] = "BOARDING"
                p["elevator_id"] = chosen_lift["id"]

        if p["state"] == "BOARDING":
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

            target_lift = next(
                (lift for lift in lifts if lift["id"] == p["elevator_id"]),
                None
            )

            if target_lift is None:
                p["state"] = "WAITING"
                p["elevator_id"] = None
                continue

            lift_x = target_lift["people_x"]

            if p["x"] > lift_x:
                p["x"] -= PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] <= lift_x:
                    p["x"] = float(lift_x)
                    p["state"] = "IN_LIFT"
            elif p["x"] < lift_x:
                p["x"] += PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] >= lift_x:
                    p["x"] = float(lift_x)
                    p["state"] = "IN_LIFT"
            else:
                p["state"] = "IN_LIFT"

            if p["state"] == "IN_LIFT" and not p["wait_recorded"]:
                completed_wait_times.append(p["wait_time"])
                recent_wait_times.append(p["wait_time"])
                p["wait_recorded"] = True

        if p["state"] == "IN_LIFT":
            target_lift = next(
                (lift for lift in lifts if lift["id"] == p["elevator_id"]),
                None
            )

            if target_lift is None:
                p["state"] = "WAITING"
                p["elevator_id"] = None
                continue

            p["floor"] = target_lift["floor"]
            p["x"] = float(target_lift["people_x"])
            p["y"] = float(floor_center_y(target_lift["floor"], floors, HEIGHT))

            if target_lift["ready"] and target_lift["floor"] == p["dest"]:
                p["state"] = "EXITING"

        if p["state"] == "EXITING":
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

            if p["x"] < exit_x:
                p["x"] += PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] >= exit_x:
                    p["x"] = float(exit_x)
                    p["state"] = "DONE"
            elif p["x"] > exit_x:
                p["x"] -= PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] <= exit_x:
                    p["x"] = float(exit_x)
                    p["state"] = "DONE"
            else:
                p["state"] = "DONE"

    people[:] = [p for p in people if p["state"] != "DONE"]


def draw_people(screen: pygame.Surface, people: list) -> None:
    for p in people:
        if p["state"] == "IN_LIFT":
            continue

        if p["state"] == "WAITING":
            color = (255, 220, 90)
        elif p["state"] == "BOARDING":
            color = (255, 160, 90)
        elif p["state"] == "EXITING":
            color = (180, 220, 255)
        else:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), PERSON_RADIUS)