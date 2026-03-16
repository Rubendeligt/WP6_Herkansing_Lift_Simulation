import pygame
import sys
import random
import inspect
import Python.People as PeopleModule

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

maybe_spawn_person = PeopleModule.maybe_spawn_person
update_people = PeopleModule.update_people
draw_people = PeopleModule.draw_people

print("People file loaded from:", PeopleModule.__file__)
print("update_people signature:", inspect.signature(update_people))


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

    shaft_w = 70
    lift_w = shaft_w
    lift_h = building_height / floors

    shaft_positions = [
        LEFT_MARGIN + 40,
        LEFT_MARGIN + 140,
        LEFT_MARGIN + 240
    ]

    lifts = [
        {
            "id": 0,
            "shaft_x": shaft_positions[0],
            "shaft_w": shaft_w,
            "lift_w": lift_w,
            "lift_h": lift_h,
            "floor_pos": 0.0,
            "dir": 1,
            "speed": LIFT_SPEED_FLOORS_PER_SEC,
            "floor": 0,
            "ready": True,
            "people_x": int(shaft_positions[0] + lift_w / 2)
        },
        {
            "id": 1,
            "shaft_x": shaft_positions[1],
            "shaft_w": shaft_w,
            "lift_w": lift_w,
            "lift_h": lift_h,
            "floor_pos": float(max(0, floors // 2)),
            "dir": -1,
            "speed": LIFT_SPEED_FLOORS_PER_SEC,
            "floor": max(0, floors // 2),
            "ready": True,
            "people_x": int(shaft_positions[1] + lift_w / 2)
        },
        {
            "id": 2,
            "shaft_x": shaft_positions[2],
            "shaft_w": shaft_w,
            "lift_w": lift_w,
            "lift_h": lift_h,
            "floor_pos": float(floors - 1),
            "dir": -1,
            "speed": LIFT_SPEED_FLOORS_PER_SEC,
            "floor": floors - 1,
            "ready": True,
            "people_x": int(shaft_positions[2] + lift_w / 2)
        }
    ]

    rng = random.Random(7)

    people = []
    waiting_lines = {}

    rest_x = RIGHT_MARGIN + 120
    call_x = shaft_positions[-1] + shaft_w + 25

    next_person_id = 1
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

                    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
                    lift_h = building_height / floors

                    for lift in lifts:
                        if lift["floor_pos"] > floors - 1:
                            lift["floor_pos"] = float(floors - 1)
                        lift["lift_h"] = lift_h
                        lift["floor"] = int(round(lift["floor_pos"]))

                if btn_plus.collidepoint(mouse_pos):
                    floors = min(MAX_FLOORS, floors + 1)
                    waiting_lines.clear()

                    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
                    lift_h = building_height / floors

                    for lift in lifts:
                        lift["lift_h"] = lift_h
                        if lift["floor_pos"] > floors - 1:
                            lift["floor_pos"] = float(floors - 1)
                        lift["floor"] = int(round(lift["floor_pos"]))

        next_person_id = maybe_spawn_person(
            rng,
            people,
            dt,
            floors,
            HEIGHT,
            rest_x,
            next_person_id
        )

        for lift in lifts:
            lift_x_for_people = lift["shaft_x"] + lift["lift_w"] / 2
            lift["people_x"] = int(lift_x_for_people)

            lift_blocked = any(
                p["state"] == "BOARDING" and p.get("elevator_id") == lift["id"]
                for p in people
            ) or any(
                p["state"] == "EXITING"
                and p.get("elevator_id") == lift["id"]
                and abs(p["x"] - lift_x_for_people) < 40
                for p in people
            )

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

        update_people(
            people,
            waiting_lines,
            dt,
            floors,
            HEIGHT,
            call_x,
            lifts
        )

        people[:] = [
            p for p in people
            if not (p["state"] == "EXITING" and p["x"] > WIDTH + 50)
        ]

        screen.fill((230, 230, 230))

        draw_building(
            screen,
            FONT,
            floors,
            HEIGHT,
            LEFT_MARGIN,
            RIGHT_MARGIN
        )

        for lift in lifts:
            passenger_count = sum(
                1
                for p in people
                if p["state"] == "IN_LIFT" and p.get("elevator_id") == lift["id"]
            )

            draw_lift(
                screen,
                lift["shaft_x"],
                lift["shaft_w"],
                lift["lift_w"],
                lift["lift_h"],
                lift["floor_pos"],
                floors,
                HEIGHT,
                passenger_count,
                FONT
            )

        draw_people(screen, people)
        draw_button(screen, FONT, btn_minus, "–")
        draw_button(screen, FONT, btn_plus, "+")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()