import pygame

MIN_FLOORS = 2
MAX_FLOORS = 24

TOP_MARGIN = 50
BOTTOM_MARGIN = 50

LEFT_MARGIN = 100

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)

PERSON_RADIUS = 8
PERSON_SPEED_PX_PER_SEC = 140

SPAWN_CHANCE_PER_SEC = 0.8

LIFT_SPEED_FLOORS_PER_SEC = 0.35

BTN_W = 70
BTN_H = 60
BTN_GAP = 12

SPAWN_RECT_X = 1400
SPAWN_RECT_Y = 50
SPAWN_RECT_W = 25
SPAWN_RECT_H = 802

MONITOR_BTN_W = 180
MONITOR_BTN_H = 50


def make_buttons(width: int):
    btn_minus = pygame.Rect(
        width - 2 * BTN_W - BTN_GAP - 40,
        30,
        BTN_W,
        BTN_H
    )

    btn_plus = pygame.Rect(
        width - BTN_W - 40,
        30,
        BTN_W,
        BTN_H
    )

    btn_monitor = pygame.Rect(
        width - MONITOR_BTN_W - 40,
        110,
        MONITOR_BTN_W,
        MONITOR_BTN_H
    )

    return btn_minus, btn_plus, btn_monitor