import pygame
from Python.Variables import GRAY, WHITE, TOP_MARGIN, BOTTOM_MARGIN


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
    LEFT_MARGIN: int,
    RIGHT_MARGIN: int,
    columns: int = 3
) -> None:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    floor_height = building_height / floors
    building_width = RIGHT_MARGIN - LEFT_MARGIN
    col_width = building_width / columns

    for row in range(floors):
        for col in range(columns):
            x = LEFT_MARGIN + col * col_width
            y = TOP_MARGIN + row * floor_height

            room = pygame.Rect(int(x), int(y), int(col_width), int(floor_height))

            pygame.draw.rect(screen, (190, 190, 190), room)
            pygame.draw.rect(screen, GRAY, room, 2)

            inner_w = room.width * 0.32
            inner_h = room.height * 0.52
            inner_x = room.x + (room.width - inner_w) / 2
            inner_y = room.y + (room.height - inner_h) / 2

            inner_rect = pygame.Rect(int(inner_x), int(inner_y), int(inner_w), int(inner_h))
            pygame.draw.rect(screen, (120, 120, 120), inner_rect)
            pygame.draw.rect(screen, (70, 70, 70), inner_rect, 2)

            pygame.draw.line(
                screen,
                (70, 70, 70),
                (inner_rect.centerx, inner_rect.top),
                (inner_rect.centerx, inner_rect.bottom),
                2
            )

    for floor in range(floors):
        y = TOP_MARGIN + floor * floor_height
        label = FONT.render(f"Floor {floors - floor - 1}", True, WHITE)
        screen.blit(label, (20, y + 5))