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
            int(self.screen_height * 0.26),
            self.tab_width,
            self.tab_height
        )


def draw_Setting_sidebar(screen, font, extra_sidebar):
    panel_rect = extra_sidebar.get_panel_rect()
    tab_rect = extra_sidebar.get_tab_rect()

    bg = (246, 247, 250)
    border = (65, 65, 75)
    title_color = (25, 25, 30)

    pygame.draw.rect(screen, bg, tab_rect, border_radius=10)
    pygame.draw.rect(screen, border, tab_rect, 2, border_radius=10)

    tab_font = pygame.font.SysFont("arial", 18, bold=True)
    tab_text = tab_font.render("Settings", True, title_color)
    rotated = pygame.transform.rotate(tab_text, 90)
    rotated_rect = rotated.get_rect(center=tab_rect.center)
    screen.blit(rotated, rotated_rect)

    pygame.draw.rect(screen, bg, panel_rect)
    pygame.draw.line(screen, border, (panel_rect.x, 0), (panel_rect.x, panel_rect.bottom), 2)