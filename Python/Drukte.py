import pygame


def get_drukte_buttons(simulation, width, height):
    panel_width = 360
    panel_x = width - panel_width - 30
    panel_y = 120

    button_map = []
    row_height = 70

    for i, period in enumerate(simulation.rush_periods):
        row_y = panel_y + 45 + i * row_height

        start_minus = pygame.Rect(panel_x + 15, row_y + 28, 28, 28)
        start_plus = pygame.Rect(panel_x + 48, row_y + 28, 28, 28)

        end_minus = pygame.Rect(panel_x + 120, row_y + 28, 28, 28)
        end_plus = pygame.Rect(panel_x + 153, row_y + 28, 28, 28)

        mult_minus = pygame.Rect(panel_x + 245, row_y + 28, 28, 28)
        mult_plus = pygame.Rect(panel_x + 278, row_y + 28, 28, 28)

        button_map.append(("start_hour_minus", i, start_minus))
        button_map.append(("start_hour_plus", i, start_plus))
        button_map.append(("end_hour_minus", i, end_minus))
        button_map.append(("end_hour_plus", i, end_plus))
        button_map.append(("multiplier_minus", i, mult_minus))
        button_map.append(("multiplier_plus", i, mult_plus))

    return button_map


def draw_drukte_panel(screen, font, simulation, width, height):
    panel_width = 360
    panel_height = 260
    panel_x = width - panel_width - 30
    panel_y = 120

    bg_color = (245, 245, 245)
    border_color = (40, 40, 40)
    text_color = (20, 20, 20)
    button_color = (220, 220, 220)

    pygame.draw.rect(screen, bg_color, (panel_x, panel_y, panel_width, panel_height), border_radius=10)
    pygame.draw.rect(screen, border_color, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)

    title = font.render("Drukte", True, text_color)
    screen.blit(title, (panel_x + 15, panel_y + 12))

    drukte_buttons = get_drukte_buttons(simulation, width, height)

    for action, idx, rect in drukte_buttons:
        pygame.draw.rect(screen, button_color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        label = "-" if "minus" in action else "+"
        label_surface = font.render(label, True, text_color)
        label_rect = label_surface.get_rect(center=rect.center)
        screen.blit(label_surface, label_rect)

    row_height = 70
    for i, period in enumerate(simulation.rush_periods):
        row_y = panel_y + 45 + i * row_height

        period_text = (
            f"Periode {i + 1}: "
            f"{period['start_hour']:02d}:{period['start_minute']:02d} - "
            f"{period['end_hour']:02d}:{period['end_minute']:02d}   "
            f"x{period['multiplier']:.1f}"
        )
        txt = font.render(period_text, True, text_color)
        screen.blit(txt, (panel_x + 15, row_y))

        screen.blit(font.render("start", True, text_color), (panel_x + 15, row_y + 60))
        screen.blit(font.render("eind", True, text_color), (panel_x + 120, row_y + 60))
        screen.blit(font.render("drukte", True, text_color), (panel_x + 245, row_y + 60))

    return drukte_buttons


def handle_drukte_click(mouse_pos, simulation, drukte_buttons):
    for action, idx, rect in drukte_buttons:
        if rect.collidepoint(mouse_pos):
            period = simulation.rush_periods[idx]

            if action == "start_hour_minus":
                simulation.set_rush_period(idx, start_hour=(period["start_hour"] - 1) % 24)
            elif action == "start_hour_plus":
                simulation.set_rush_period(idx, start_hour=(period["start_hour"] + 1) % 24)
            elif action == "end_hour_minus":
                simulation.set_rush_period(idx, end_hour=(period["end_hour"] - 1) % 24)
            elif action == "end_hour_plus":
                simulation.set_rush_period(idx, end_hour=(period["end_hour"] + 1) % 24)
            elif action == "multiplier_minus":
                simulation.set_rush_period(idx, multiplier=max(0.5, period["multiplier"] - 0.5))
            elif action == "multiplier_plus":
                simulation.set_rush_period(idx, multiplier=min(10.0, period["multiplier"] + 0.5))

            return True

    return False