import random
import pygame
from Python.Variables import TOP_MARGIN, BOTTOM_MARGIN, PERSON_RADIUS, PERSON_SPEED_PX_PER_SEC, SPAWN_CHANCE_PER_SEC

def floor_center_y(floor_index: int, floors: int, HEIGHT: int) -> float:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / floors
    return TOP_MARGIN + floor_index * FLOOR_HEIGHT + FLOOR_HEIGHT / 2

def maybe_spawn_person(
    rng: random.Random,
    people: list,
    dt: float,
    floors: int,
    HEIGHT: int,
    rest_x: int,
    next_person_id: int
) -> int:
    if rng.random() < SPAWN_CHANCE_PER_SEC * dt:
        start_floor = rng.randrange(0, floors)
        y = floor_center_y(start_floor, floors, HEIGHT)

        dest_floor = rng.randrange(0, floors)
        while dest_floor == start_floor and floors > 1:
            dest_floor = rng.randrange(0, floors)

        people.append({
            "id": next_person_id,
            "floor": start_floor,
            "dest": dest_floor,
            "x": float(rest_x),
            "y": float(y),
            "state": "WALKING" 
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
    lift_floor: int,
    lift_ready: bool,
    lift_x: int
) -> None:
    spacing = PERSON_RADIUS * 2 + 6
    waiting_lines.clear()

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
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

            waiting_lines.setdefault(p["floor"], []).append(p["id"])
            idx = waiting_lines[p["floor"]].index(p["id"])
            p["x"] = float(call_x + idx * spacing)

            if lift_ready and p["floor"] == lift_floor:
                p["state"] = "IN_LIFT"

        if p["state"] == "IN_LIFT":
            # “plakken” aan lift
            p["floor"] = lift_floor
            p["x"] = float(lift_x)
            p["y"] = float(floor_center_y(lift_floor, floors, HEIGHT))

            if lift_ready and lift_floor == p["dest"]:
                p["state"] = "EXITING"

        if p["state"] == "EXITING":
            p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))
            p["x"] += PERSON_SPEED_PX_PER_SEC * dt

def draw_people(screen: pygame.Surface, people: list) -> None:
    for p in people:
        if p["state"] == "WAITING":
            color = (255, 220, 90)
        elif p["state"] == "IN_LIFT":
            color = (90, 180, 255)
        else:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), PERSON_RADIUS)