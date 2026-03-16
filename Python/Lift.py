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
    cab = pygame.Rect(shaft_x, y, lift_w, lift_h)

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