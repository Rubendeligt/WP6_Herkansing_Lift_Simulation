import random
import pygame
from Python.Variables import TOP_MARGIN, BOTTOM_MARGIN, PERSON_RADIUS, PERSON_SPEED_PX_PER_SEC, SPAWN_CHANCE_PER_SEC

def floor_center_y(floor_index: int, floors: int, HEIGHT: int) -> float:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / floors
    return TOP_MARGIN + floor_index * FLOOR_HEIGHT + FLOOR_HEIGHT / 2

def maybe_spawn_person(rng: random.Random, people: list, dt: float, floors: int, HEIGHT: int, rest_x: int, next_person_id: int) -> int:
    if rng.random() < SPAWN_CHANCE_PER_SEC * dt:
        floor_index = rng.randrange(0, floors)
        y = floor_center_y(floor_index, floors, HEIGHT)

        people.append({
            "id": next_person_id,
            "floor": floor_index,
            "x": float(rest_x),
            "y": float(y),
            "state": "WALKING"
        })
        next_person_id += 1
    return next_person_id

def update_people(people: list, waiting_lines: dict, dt: float, floors: int, HEIGHT: int, call_x: int) -> None:
    spacing = PERSON_RADIUS * 2 + 6

    for p in people:
        if p["floor"] > floors - 1:
            p["floor"] = floors - 1
        if p["floor"] < 0:
            p["floor"] = 0

        p["y"] = float(floor_center_y(p["floor"], floors, HEIGHT))

        if p["state"] == "WALKING":
            if p["x"] > call_x:
                p["x"] -= PERSON_SPEED_PX_PER_SEC * dt
                if p["x"] <= call_x:
                    p["x"] = float(call_x)
                    p["state"] = "WAITING"

                    if p["floor"] not in waiting_lines:
                        waiting_lines[p["floor"]] = []
                    if p["id"] not in waiting_lines[p["floor"]]:
                        waiting_lines[p["floor"]].append(p["id"])

        if p["state"] == "WAITING":
            if p["floor"] not in waiting_lines:
                waiting_lines[p["floor"]] = []
            if p["id"] not in waiting_lines[p["floor"]]:
                waiting_lines[p["floor"]].append(p["id"])

            idx = waiting_lines[p["floor"]].index(p["id"])
            p["x"] = float(call_x + idx * spacing)

def draw_people(screen: pygame.Surface, people: list) -> None:
    for p in people:
        color = (255, 220, 90) if p["state"] == "WAITING" else (255, 255, 255)
        pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), PERSON_RADIUS)