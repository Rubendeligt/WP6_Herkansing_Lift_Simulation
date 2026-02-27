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

def draw_building(screen: pygame.Surface, FONT: pygame.font.Font, floors: int, HEIGHT: int, LEFT_MARGIN: int, RIGHT_MARGIN: int) -> None:
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / floors

    for floor in range(floors):
        y = TOP_MARGIN + floor * FLOOR_HEIGHT
        pygame.draw.line(screen, GRAY, (LEFT_MARGIN, y), (RIGHT_MARGIN, y), 2)

        label = FONT.render(f"Floor {floors - floor - 1}", True, WHITE)
        screen.blit(label, (20, y - 10))