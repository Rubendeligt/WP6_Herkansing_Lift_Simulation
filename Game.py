import pygame
import sys
import random

from Python.Variables import (
    MIN_FLOORS,
    MAX_FLOORS,
    LEFT_MARGIN,
    RIGHT_MARGIN_DEFAULT,
    LIFT_SPEED_FLOORS_PER_SEC,
    make_buttons,
    TOP_MARGIN,
    BOTTOM_MARGIN
)
from Python.Draw import draw_building, draw_button
from Python.Lift import draw_lift, update_lift
from Python.People import maybe_spawn_person, update_people, draw_people


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Lift Simulator")

    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("arial", 18)

    floors = 4

    btn_minus, btn_plus = make_buttons(WIDTH)

    RIGHT_MARGIN = RIGHT_MARGIN_DEFAULT

    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN

    shaft_x = LEFT_MARGIN + 50
    shaft_w = 80
    lift_w = shaft_w
    lift_h = building_height / floors

    lift_floor_pos = 0.0
    lift_dir = 1
    lift_speed_floors_per_sec = LIFT_SPEED_FLOORS_PER_SEC

    rng = random.Random(7)

    people = []
    waiting_lines = {}

    rest_x = RIGHT_MARGIN + 120
    call_x = shaft_x + shaft_w + 25

    next_person_id = 1
    door_progress = 0.0
    door_hold_timer = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if btn_minus.collidepoint(mouse_pos):
                    floors = max(MIN_FLOORS, floors - 1)
                    waiting_lines.clear()

                    if lift_floor_pos > floors - 1:
                        lift_floor_pos = float(floors - 1)

                    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
                    lift_h = building_height / floors

                if btn_plus.collidepoint(mouse_pos):
                    floors = min(MAX_FLOORS, floors + 1)
                    waiting_lines.clear()

                    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
                    lift_h = building_height / floors

        next_person_id = maybe_spawn_person(
            rng,
            people,
            dt,
            floors,
            HEIGHT,
            rest_x,
            next_person_id
        )

        cab_x = shaft_x
        lift_x_for_people = cab_x + lift_w / 2

        lift_blocked = any(p["state"] == "BOARDING" for p in people) or any(
            p["state"] == "EXITING" and abs(p["x"] - lift_x_for_people) < 40
            for p in people
        )

        if not lift_blocked:
            lift_floor_pos, lift_dir = update_lift(
                lift_floor_pos,
                lift_dir,
                lift_speed_floors_per_sec,
                dt,
                floors
            )

        lift_floor_int = int(round(lift_floor_pos))
        lift_ready = abs(lift_floor_pos - lift_floor_int) < 0.03

        boarding = any(p["state"] == "BOARDING" for p in people)
        exiting = any(
            p["state"] == "EXITING" and abs(p["x"] - lift_x_for_people) < 35
            for p in people
        )

        if lift_ready and boarding:
            door_hold_timer = 1.8
        elif lift_ready and exiting:
            door_hold_timer = 1.0
        elif door_hold_timer > 0:
            door_hold_timer = max(0.0, door_hold_timer - dt)

        doors_should_be_open = lift_ready and (
            boarding or exiting or door_hold_timer > 0
        )

        if doors_should_be_open:
            door_progress = min(1.0, door_progress + 3 * dt)
        else:
            door_progress = max(0.0, door_progress - 4 * dt)

        update_people(
            people,
            waiting_lines,
            dt,
            floors,
            HEIGHT,
            call_x,
            lift_floor_int,
            lift_ready,
            int(lift_x_for_people)
        )

        people[:] = [
            p for p in people
            if not (p["state"] == "EXITING" and p["x"] > WIDTH + 50)
        ]

        screen.fill((230, 230, 230))

        passenger_count = sum(1 for p in people if p["state"] == "IN_LIFT")

        draw_building(
            screen,
            FONT,
            floors,
            HEIGHT,
            LEFT_MARGIN,
            RIGHT_MARGIN
        )

        draw_lift(
            screen,
            shaft_x,
            shaft_w,
            lift_w,
            lift_h,
            lift_floor_pos,
            floors,
            HEIGHT,
            passenger_count,
            FONT,
            door_progress
        )

        draw_people(screen, people)
        draw_button(screen, FONT, btn_minus, "–")
        draw_button(screen, FONT, btn_plus, "+")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()