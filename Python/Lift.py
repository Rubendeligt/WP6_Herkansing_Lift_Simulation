import pygame
from Python.Variables import GRAY, TOP_MARGIN, BOTTOM_MARGIN

def floor_to_y(floor_pos: float, floors: int, HEIGHT: int) -> float:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / floors
    return TOP_MARGIN + (floors - 1 - floor_pos) * FLOOR_HEIGHT

def update_lift(lift_floor_pos: float, lift_dir: int, lift_speed_floors_per_sec: float, dt: float, floors: int) -> tuple[float, int]:
    lift_floor_pos += lift_dir * lift_speed_floors_per_sec * dt

    if lift_floor_pos >= floors - 1:
        lift_floor_pos = float(floors - 1)
        lift_dir = -1

    if lift_floor_pos <= 0:
        lift_floor_pos = 0.0
        lift_dir = 1

    return lift_floor_pos, lift_dir

def draw_lift(screen: pygame.Surface, shaft_x: int, shaft_w: int, lift_w: int, lift_h: int, lift_floor_pos: float, floors: int, HEIGHT: int) -> None:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    pygame.draw.rect(screen, GRAY, pygame.Rect(shaft_x, TOP_MARGIN, shaft_w, BUILDING_HEIGHT), 2)

    y = floor_to_y(lift_floor_pos, floors, HEIGHT)
    cab = pygame.Rect(shaft_x + 10, y + 5, lift_w, lift_h)
    pygame.draw.rect(screen, (80, 220, 120), cab, border_radius=8)