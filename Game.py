import pygame
import sys
import random

def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Lift Simulator")

    btn_w, btn_h = 70, 60
    btn_gap = 12
    btn_minus = pygame.Rect(WIDTH - 2 * btn_w - btn_gap - 40, 30, btn_w, btn_h)
    btn_plus  = pygame.Rect(WIDTH - btn_w - 40, 30, btn_w, btn_h)
    MIN_FLOORS = 2
    MAX_FLOORS = 24

    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("arial", 18)

    floors = 10
    TOP_MARGIN = 50
    BOTTOM_MARGIN = 50

    LEFT_MARGIN = 100
    RIGHT_MARGIN = 700

    WHITE = (255, 255, 255)
    BLACK = (20, 20, 20)
    GRAY = (120, 120, 120)

    shaft_x = LEFT_MARGIN - 120
    shaft_w = 80
    lift_w = shaft_w - 20
    lift_h = 30
    people = []
    waiting_lines = { }
    lift_floor_pos = 0.0
    lift_dir = 1
    lift_speed_floors_per_sec = 0.8

    rng = random.Random(7)

    people = []
    person_radius = 8
    person_speed_px_per_sec = 140

    rest_x = RIGHT_MARGIN + 180
    call_x = shaft_x + shaft_w + 25

    spawn_chance_per_sec = 0.8
    next_person_id = 1

    def draw_button(rect: pygame.Rect, text: str) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = (160, 160, 160) if rect.collidepoint(mouse_pos) else (200, 200, 200)

        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), rect, width=2, border_radius=10)

        label = FONT.render(text, True, (20, 20, 20))
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def floor_to_y(floor_pos: float) -> float:
        BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        FLOOR_HEIGHT = BUILDING_HEIGHT / floors
        return TOP_MARGIN + (floors - 1 - floor_pos) * FLOOR_HEIGHT

    def floor_center_y(floor_index: int) -> float:
        BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        FLOOR_HEIGHT = BUILDING_HEIGHT / floors
        return TOP_MARGIN + floor_index * FLOOR_HEIGHT + FLOOR_HEIGHT / 2

    def draw_building():
        """
        en toont het verdiepingsnummer.
        """
        BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        FLOOR_HEIGHT = BUILDING_HEIGHT / floors

        for floor in range(floors):
            y = TOP_MARGIN + floor * FLOOR_HEIGHT

            pygame.draw.line(screen, GRAY, (LEFT_MARGIN, y), (RIGHT_MARGIN, y), 2)
            label = FONT.render(f"Floor {floors - floor - 1}", True, WHITE)
            screen.blit(label, (20, y - 10))

    def draw_lift():
        BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        pygame.draw.rect(screen, GRAY, pygame.Rect(shaft_x, TOP_MARGIN, shaft_w, BUILDING_HEIGHT), 2)

        y = floor_to_y(lift_floor_pos)
        cab = pygame.Rect(shaft_x + 10, y + 5, lift_w, lift_h)
        pygame.draw.rect(screen, (80, 220, 120), cab, border_radius=8)

    def maybe_spawn_person(dt: float) -> None:
        nonlocal next_person_id

        if rng.random() < spawn_chance_per_sec * dt:
            floor_index = rng.randrange(0, floors)
            y = floor_center_y(floor_index)

            people.append({
                "id": next_person_id,
                "floor": floor_index,
                "x": float(rest_x),
                "y": float(y),
                "state": "WALKING"
            })
            next_person_id += 1

    def update_people(dt: float) -> None:
        spacing = person_radius * 2 + 6

        for p in people:
            if p["floor"] > floors - 1:
                p["floor"] = floors - 1
            if p["floor"] < 0:
                p["floor"] = 0

            p["y"] = float(floor_center_y(p["floor"]))

            if p["state"] == "WALKING":
                if p["x"] > call_x:
                    p["x"] -= person_speed_px_per_sec * dt
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

    def draw_people() -> None:
        for p in people:
            color = (255, 220, 90) if p["state"] == "WAITING" else (255, 255, 255)
            pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), person_radius)

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

                if btn_plus.collidepoint(mouse_pos):
                    floors = min(MAX_FLOORS, floors + 1)
                    waiting_lines.clear()

        lift_floor_pos += lift_dir * lift_speed_floors_per_sec * dt

        if lift_floor_pos >= floors - 1:
            lift_floor_pos = float(floors - 1)
            lift_dir = -1

        if lift_floor_pos <= 0:
            lift_floor_pos = 0.0
            lift_dir = 1

        maybe_spawn_person(dt)
        update_people(dt)

        screen.fill(BLACK)

        draw_building()
        draw_lift()
        draw_people()
        draw_button(btn_minus, "–")
        draw_button(btn_plus, "+")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()