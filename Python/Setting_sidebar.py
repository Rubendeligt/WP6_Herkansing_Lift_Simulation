import pygame


class SettingSidebar:
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
            int(self.screen_height * 0.16),
            self.tab_width,
            self.tab_height
        )

    def get_button_rects(self):
        panel_rect = self.get_panel_rect()

        button_width = 220
        button_height = 42
        left = panel_rect.x + 50
        start_y = 120
        gap = 16

        btn_minus = pygame.Rect(left, start_y + 0 * (button_height + gap), button_width, button_height)
        btn_plus = pygame.Rect(left, start_y + 1 * (button_height + gap), button_width, button_height)
        btn_add_normal_lift = pygame.Rect(left, start_y + 2 * (button_height + gap), button_width, button_height)
        btn_add_fast_lift = pygame.Rect(left, start_y + 3 * (button_height + gap), button_width, button_height)
        btn_remove_lift = pygame.Rect(left, start_y + 4 * (button_height + gap), button_width, button_height)
        btn_restart_day = pygame.Rect(left, start_y + 5 * (button_height + gap), button_width, button_height)

        return (
            btn_minus,
            btn_plus,
            btn_add_normal_lift,
            btn_add_fast_lift,
            btn_remove_lift,
            btn_restart_day,
        )


def draw_Setting_sidebar(screen, font, setting_sidebar):
    panel_rect = setting_sidebar.get_panel_rect()
    tab_rect = setting_sidebar.get_tab_rect()

    bg = (246, 247, 250)
    border = (65, 65, 75)
    title_color = (25, 25, 30)
    text_color = (85, 85, 95)
    section_bg = (255, 255, 255)
    soft = (220, 222, 228)

    pygame.draw.rect(screen, bg, tab_rect, border_radius=10)
    pygame.draw.rect(screen, border, tab_rect, 2, border_radius=10)

    tab_font = pygame.font.SysFont("arial", 18, bold=True)
    tab_text = tab_font.render("Settings", True, title_color)
    rotated = pygame.transform.rotate(tab_text, 90)
    rotated_rect = rotated.get_rect(center=tab_rect.center)
    screen.blit(rotated, rotated_rect)

    pygame.draw.rect(screen, bg, panel_rect)
    pygame.draw.line(screen, border, (panel_rect.x, 0), (panel_rect.x, panel_rect.bottom), 2)
    title_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    screen.blit(title_font.render("Settings", True, title_color), (panel_rect.x + 20, 22))
    screen.blit(
        small_font.render("Bediening van de simulatie", True, text_color),
        (panel_rect.x + 20, 54)
    )

    box = pygame.Rect(panel_rect.x + 18, 95, panel_rect.width - 36, 330)
    pygame.draw.rect(screen, section_bg, box, border_radius=14)
    pygame.draw.rect(screen, soft, box, 1, border_radius=14)