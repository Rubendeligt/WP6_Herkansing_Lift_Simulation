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
    shaft_positions: list[int],
    shaft_w: int
) -> None:
    building_height = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    floor_height = building_height / floors

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