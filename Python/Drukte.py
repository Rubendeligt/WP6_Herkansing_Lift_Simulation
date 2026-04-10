import pygame


class DruktePanel:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panel_width = 360
        self.panel_height = screen_height
        self.closed_x = screen_width
        self.open_x = screen_width - self.panel_width
        self.x = self.closed_x

        self.y = 0
        self.speed = 900
        self.is_open = False

        self.tab_width = 40
        self.tab_height = 140

    def update(self, dt: float) -> None:
        target_x = self.open_x if self.is_open else self.closed_x

        if self.x < target_x:
            self.x += self.speed * dt
            if self.x > target_x:
                self.x = target_x
        elif self.x > target_x:
            self.x -= self.speed * dt
            if self.x < target_x:
                self.x = target_x

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.get_tab_rect().collidepoint(event.pos):
                self.is_open = not self.is_open

    def get_panel_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), self.y, self.panel_width, self.panel_height)

    def get_tab_rect(self) -> pygame.Rect:
        panel_rect = self.get_panel_rect()
        return pygame.Rect(
            panel_rect.x - self.tab_width,
            int(self.screen_height * 0.68),
            self.tab_width,
            self.tab_height
        )
    
def get_drukte_buttons(simulation, drukte_panel):
    panel_rect = drukte_panel.get_panel_rect()

    button_map = []
    row_height = 95
    start_y = 110

    for i, period in enumerate(simulation.rush_periods):
        row_y = panel_rect.y + start_y + i * row_height

        start_minus = pygame.Rect(panel_rect.x + 24, row_y + 42, 30, 30)
        start_plus = pygame.Rect(panel_rect.x + 60, row_y + 42, 30, 30)

        end_minus = pygame.Rect(panel_rect.x + 140, row_y + 42, 30, 30)
        end_plus = pygame.Rect(panel_rect.x + 176, row_y + 42, 30, 30)

        mult_minus = pygame.Rect(panel_rect.x + 274, row_y + 42, 30, 30)
        mult_plus = pygame.Rect(panel_rect.x + 310, row_y + 42, 30, 30)

        button_map.append(("start_hour_minus", i, start_minus))
        button_map.append(("start_hour_plus", i, start_plus))
        button_map.append(("end_hour_minus", i, end_minus))
        button_map.append(("end_hour_plus", i, end_plus))
        button_map.append(("multiplier_minus", i, mult_minus))
        button_map.append(("multiplier_plus", i, mult_plus))

    return button_map

def draw_drukte_panel(screen, font, simulation, drukte_panel):
    panel_rect = drukte_panel.get_panel_rect()
    tab_rect = drukte_panel.get_tab_rect()

    bg = (246, 247, 250)
    border = (65, 65, 75)
    title_color = (25, 25, 30)
    text = (85, 85, 95)
    soft = (220, 222, 228)
    card = (255, 255, 255)
    button = (236, 238, 242)
    hover = (220, 223, 230)

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, bg, tab_rect, border_radius=10)
    pygame.draw.rect(screen, border, tab_rect, 2, border_radius=10)

    tab_font = pygame.font.SysFont("arial", 18, bold=True)
    tab_text = tab_font.render("Drukte", True, title_color)
    rotated = pygame.transform.rotate(tab_text, 90)
    rotated_rect = rotated.get_rect(center=tab_rect.center)
    screen.blit(rotated, rotated_rect)
    pygame.draw.rect(screen, bg, panel_rect)
    pygame.draw.line(screen, border, (panel_rect.x, 0), (panel_rect.x, panel_rect.bottom), 2)

    title_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    screen.blit(title_font.render("Drukte paneel", True, title_color), (panel_rect.x + 20, 22))
    screen.blit(
        small_font.render("Pas de drukke momenten aan", True, text),
        (panel_rect.x + 20, 54)
    )

    drukte_buttons = get_drukte_buttons(simulation, drukte_panel)

    row_height = 95
    start_y = 110

    for i, period in enumerate(simulation.rush_periods):
        row_y = panel_rect.y + start_y + i * row_height

        card_rect = pygame.Rect(panel_rect.x + 14, row_y, panel_rect.width - 28, 78)
        pygame.draw.rect(screen, card, card_rect, border_radius=14)
        pygame.draw.rect(screen, soft, card_rect, 1, border_radius=14)

        label = small_font.render(f"Periode {i + 1}", True, text)
        screen.blit(label, (card_rect.x + 12, card_rect.y + 10))

        info = f"{period['start_hour']:02d}:00 - {period['end_hour']:02d}:00    x{period['multiplier']:.1f}"
        info_surface = small_font.render(info, True, title_color)
        screen.blit(info_surface, (card_rect.x + 12, card_rect.y + 30))

        screen.blit(small_font.render("start", True, text), (panel_rect.x + 24, row_y + 22))
        screen.blit(small_font.render("eind", True, text), (panel_rect.x + 140, row_y + 22))
        screen.blit(small_font.render("drukte", True, text), (panel_rect.x + 258, row_y + 22))

    for action, idx, rect in drukte_buttons:
        color = hover if rect.collidepoint(mouse_pos) else button
        pygame.draw.rect(screen, color, rect, border_radius=7)
        pygame.draw.rect(screen, border, rect, 1, border_radius=7)

        label = "-" if "minus" in action else "+"
        txt = font.render(label, True, (20, 20, 20))
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)

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