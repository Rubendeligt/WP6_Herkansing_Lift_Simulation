import pygame
from Python.Variables import (
    GRAY,
    TOP_MARGIN,
    BOTTOM_MARGIN,
    DOOR_OPEN_SPEED,
    DOOR_CLOSE_SPEED,
    DOOR_HOLD_BOARDING,
    DOOR_HOLD_EXITING,
    EXIT_NEAR_LIFT_DISTANCE
)


def floor_to_y(floor_pos: float, floors: int, HEIGHT: int) -> float:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / floors
    return TOP_MARGIN + (floors - 1 - floor_pos) * FLOOR_HEIGHT


def update_lift(
    lift_floor_pos: float,
    lift_dir: int,
    lift_speed_floors_per_sec: float,
    dt: float,
    floors: int
) -> tuple[float, int]:
    lift_floor_pos += lift_dir * lift_speed_floors_per_sec * dt

    if lift_floor_pos >= floors - 1:
        lift_floor_pos = float(floors - 1)
        lift_dir = -1

    if lift_floor_pos <= 0:
        lift_floor_pos = 0.0
        lift_dir = 1

    return lift_floor_pos, lift_dir


def get_lift_ready(lift_floor_pos: float) -> tuple[int, bool]:
    lift_floor_int = int(round(lift_floor_pos))
    lift_ready = abs(lift_floor_pos - lift_floor_int) < 0.03
    return lift_floor_int, lift_ready


def update_lift_doors(
    people: list,
    lift_x_for_people: float,
    lift_ready: bool,
    door_progress: float,
    door_hold_timer: float,
    dt: float
) -> tuple[float, float, bool]:
    boarding = any(p["state"] == "BOARDING" for p in people)

    exiting = any(
        p["state"] == "EXITING" and abs(p["x"] - lift_x_for_people) < EXIT_NEAR_LIFT_DISTANCE
        for p in people
    )

    if lift_ready and boarding:
        door_hold_timer = DOOR_HOLD_BOARDING
    elif lift_ready and exiting:
        door_hold_timer = DOOR_HOLD_EXITING
    elif door_hold_timer > 0:
        door_hold_timer = max(0.0, door_hold_timer - dt)

    doors_should_be_open = lift_ready and (
        boarding or exiting or door_hold_timer > 0
    )

    if doors_should_be_open:
        door_progress = min(1.0, door_progress + DOOR_OPEN_SPEED * dt)
    else:
        door_progress = max(0.0, door_progress - DOOR_CLOSE_SPEED * dt)

    lift_blocked = boarding or exiting or door_hold_timer > 0

    return door_progress, door_hold_timer, lift_blocked


def draw_lift(
    screen: pygame.Surface,
    shaft_x: int,
    shaft_w: int,
    lift_w: int,
    lift_h: int,
    lift_floor_pos: float,
    floors: int,
    HEIGHT: int,
    passenger_count: int,
    FONT: pygame.font.Font,
    door_open: float = 0.0
) -> None:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    pygame.draw.rect(screen, GRAY, pygame.Rect(shaft_x, TOP_MARGIN, shaft_w, BUILDING_HEIGHT), 2)

    y = floor_to_y(lift_floor_pos, floors, HEIGHT)
    cab = pygame.Rect(int(shaft_x), int(y), int(lift_w), int(lift_h))

    pygame.draw.rect(screen, (0, 0, 0), cab, border_radius=8)

    inner = cab.inflate(-10, -10)
    pygame.draw.rect(screen, (200, 200, 200), inner)

    open_amount = max(0.0, min(1.0, door_open))
    half_w = cab.w / 2
    door_w = int(half_w * (1 - open_amount))

    left_door = pygame.Rect(cab.x, cab.y, door_w, cab.h)
    right_door = pygame.Rect(cab.right - door_w, cab.y, door_w, cab.h)

    pygame.draw.rect(screen, (30, 30, 30), left_door)
    pygame.draw.rect(screen, (30, 30, 30), right_door)

    label = FONT.render(str(passenger_count), True, (255, 255, 255))
    label_rect = label.get_rect(center=cab.center)
    screen.blit(label, label_rect)