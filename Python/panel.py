import pygame


def make_floor_buttons(floors, start_x, start_y):

    buttons = []
    size = 40
    gap = 10

    for i in range(floors):

        x = start_x + (i % 4) * (size + gap)
        y = start_y + (i // 4) * (size + gap)

        rect = pygame.Rect(x, y, size, size)

        buttons.append({
            "floor": i,
            "rect": rect,
            "active": False
        })

    return buttons


def draw_floor_buttons(screen, FONT, buttons):

    for b in buttons:

        if b["active"]:
            color = (100, 200, 100)
        else:
            color = (180, 180, 180)

        pygame.draw.rect(screen, color, b["rect"], border_radius=6)

        label = FONT.render(str(b["floor"]), True, (20, 20, 20))
        screen.blit(label, label.get_rect(center=b["rect"].center))