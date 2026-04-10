import pygame


def draw_lift_hover_info(screen, font, simulation, hovered_lift_id, hovered_lift_rect):
    if hovered_lift_id is None or hovered_lift_rect is None:
        return

    destinations = simulation.get_lift_destinations(hovered_lift_id)

    current_lift = next(
        (lift for lift in simulation.lifts if lift["id"] == hovered_lift_id),
        None
    )

    if current_lift is None:
        return

    shown_current_floor = current_lift["floor"] + 1

    lines = [
        f"Lift {hovered_lift_id + 1}",
        f"Nu op: {shown_current_floor}"
    ]

    if not destinations:
        lines.append("Geen passagiers")
    else:
        for dest, count in destinations.items():
            shown_floor = dest + 1
            if count == 1:
                lines.append(f"1 wil naar {shown_floor}")
            else:
                lines.append(f"{count} willen naar {shown_floor}")

    padding = 10
    line_height = 24
    width = 210
    height = padding * 2 + len(lines) * line_height

    x = hovered_lift_rect.right + 15
    y = hovered_lift_rect.top

    if x + width > simulation.width:
        x = hovered_lift_rect.left - width - 15

    if y + height > simulation.height:
        y = simulation.height - height - 10

    box_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, (245, 245, 245), box_rect, border_radius=10)
    pygame.draw.rect(screen, (40, 40, 40), box_rect, 2, border_radius=10)

    for i, text in enumerate(lines):
        surf = font.render(text, True, (20, 20, 20))
        screen.blit(surf, (x + padding, y + padding + i * line_height))