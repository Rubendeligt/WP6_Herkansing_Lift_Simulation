import pygame
from Python.Variables import GRAY, TOP_MARGIN, BOTTOM_MARGIN

def floor_to_y(floor_pos: float, floors: int, HEIGHT: int, lift_h: float) -> float:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    floor_height = building_height / floors
    floor_top = TOP_MARGIN + (floors - 1 - floor_pos) * floor_height
    return floor_top + (floor_height - lift_h) / 2

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
    lift_h: float,
    lift_floor_pos: float,
    floors: int,
    HEIGHT: int,
    passenger_count: int,
    FONT: pygame.font.Font,
    lift_type: str
) -> pygame.Rect:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    pygame.draw.rect(screen, GRAY, pygame.Rect(shaft_x, TOP_MARGIN, shaft_w, building_height), 2)

    y = floor_to_y(lift_floor_pos, floors, HEIGHT, lift_h)
    cab_w = int(shaft_w * 0.92)
    cab_x = shaft_x + (shaft_w - cab_w) / 2
    cab = pygame.Rect(int(cab_x), int(y), int(cab_w), int(lift_h))

    if lift_type == "fast":
        fill_color = (255, 170, 70)
        border_color = (180, 90, 20)
    else:
        fill_color = (80, 220, 120)
        border_color = (40, 140, 70)

    pygame.draw.rect(screen, fill_color, cab, border_radius=8)
    pygame.draw.rect(screen, border_color, cab, 2, border_radius=8)

    label = FONT.render(str(passenger_count), True, (20, 20, 20))
    label_rect = label.get_rect(center=cab.center)
    screen.blit(label, label_rect)

    return cab