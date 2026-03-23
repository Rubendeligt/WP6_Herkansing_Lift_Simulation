import pygame
from Python.Variables import GRAY, WHITE, TOP_MARGIN, BOTTOM_MARGIN
from Python.grafiek import draw_wait_time_graph, draw_people_graph

def draw_button(screen: pygame.Surface, FONT: pygame.font.Font, rect: pygame.Rect, text: str) -> None:
    mouse_pos = pygame.mouse.get_pos()
    color = (160, 160, 160) if rect.collidepoint(mouse_pos) else (200, 200, 200)

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (120, 120, 120), rect, width=2, border_radius=10)

    label = FONT.render(text, True, (20, 20, 20))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_building(
    screen: pygame.Surface,
    FONT: pygame.font.Font,
    floors: int,
    HEIGHT: int,
    shaft_positions: list[int],
    shaft_w: int
) -> None:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    floor_height = building_height / floors

    left = shaft_positions[0]
    right = screen.get_width() - 200
    corridor_x = shaft_positions[-1] + shaft_w
    corridor_rect = pygame.Rect(
        int(corridor_x),
        int(TOP_MARGIN),
        int(right - corridor_x),
        int(building_height)
    )
    pygame.draw.rect(screen, (230, 222, 220), corridor_rect)

    for row in range(floors):
        y = TOP_MARGIN + row * floor_height

        for shaft_x in shaft_positions:
            room = pygame.Rect(
                int(shaft_x),
                int(y),
                int(shaft_w),
                int(floor_height)
            )

            pygame.draw.rect(screen, (190, 190, 190), room)
            pygame.draw.rect(screen, GRAY, room, 2)

            door_w = room.width * 0.7
            door_h = room.height * 0.6
            door_x = room.x + (room.width - door_w) / 2
            door_y = room.y + (room.height - door_h) / 2

            door_rect = pygame.Rect(
                int(door_x),
                int(door_y),
                int(door_w),
                int(door_h)
            )

            pygame.draw.rect(screen, (120, 120, 120), door_rect)
            pygame.draw.rect(screen, (70, 70, 70), door_rect, 2)

            pygame.draw.line(
                screen,
                (70, 70, 70),
                (door_rect.centerx, door_rect.top),
                (door_rect.centerx, door_rect.bottom),
                2
            )

    for floor in range(floors):
        y = TOP_MARGIN + floor * floor_height
        label = FONT.render(f"Floor {floors - floor - 1}", True, WHITE)
        screen.blit(label, (20, y + 5))

    for floor in range(floors + 1):
        y = TOP_MARGIN + floor * floor_height

        left = shaft_positions[0]
        right = shaft_positions[-1] + shaft_w + 600

        pygame.draw.line(
            screen,
            (120, 120, 130),
            (left, y),
            (right, y),
            2
        )

    top = TOP_MARGIN
    bottom = TOP_MARGIN + building_height

    right = screen.get_width() - 200 

    pygame.draw.line(
        screen,
        (120, 120, 130),
        (right, top),
        (right, bottom),
        2
)
    pygame.draw.rect(screen, (0, 0, 0), (1400, 50, 25, 802))
def draw_information_panel(screen, info_panel, font, simulation):
    button = info_panel.get_button_rect()
    pygame.draw.rect(screen, (90, 90, 90), button, border_radius=6)

    arrow = "<" if info_panel.open else ">"
    text = font.render(arrow, True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=button.center))

    panel = info_panel.get_panel_rect()
    pygame.draw.rect(screen, (25, 25, 35), panel)

    title = font.render("Information", True, (255, 255, 255))
    screen.blit(title, (panel.x + 20, 20))

    floors = font.render(f"Floors: {simulation.floors}", True, (200, 200, 200))
    screen.blit(floors, (panel.x + 20, 70))

    lifts = font.render(f"Lifts: {simulation.total_lifts}", True, (200, 200, 200))
    screen.blit(lifts, (panel.x + 20, 110))

    people = font.render(f"People: {len(simulation.people)}", True, (200, 200, 200))
    screen.blit(people, (panel.x + 20, 150))

    avg_wait = simulation.get_average_wait_time()
    avg_wait_text = font.render(
    f"Gem. wachttijd: {avg_wait:.1f}s",
    True,
    (200, 200, 200)
)
    screen.blit(avg_wait_text, (panel.x + 20, 190))
    time_text = font.render(f"Tijd: {simulation.get_time_string()}", True, (255, 255, 255))
    screen.blit(time_text, (20, 20)) 

    draw_wait_time_graph(screen, panel, font, simulation)
    draw_people_graph(screen, panel, font, simulation)

def draw_time(screen, font, simulation):
    time_str = simulation.get_time_string()
    text = font.render(time_str, True, (255, 255, 255))
    text_rect = text.get_rect()
    screen_width = screen.get_width()
    text_rect.midtop = (screen_width // 2, 10)
    padding = 10
    bg_rect = text_rect.inflate(padding * 2, padding)

    pygame.draw.rect(screen, (0, 0, 0), bg_rect, border_radius=8)
    screen.blit(text, text_rect)