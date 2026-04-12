import pygame


class InformationPanel:
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height

        self.width = 420
        self.button_w = 35
        self.button_h = 120

        self.open = False
        self.speed = 800

        self.x = width
        self.target_x = width

        self.active_filter = "all"

    def toggle(self):
        self.open = not self.open
        if self.open:
            self.target_x = self.screen_width - self.width
        else:
            self.target_x = self.screen_width

    def update(self, dt):
        if self.x < self.target_x:
            self.x += self.speed * dt
            if self.x > self.target_x:
                self.x = self.target_x

        elif self.x > self.target_x:
            self.x -= self.speed * dt
            if self.x < self.target_x:
                self.x = self.target_x

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_rect = self.get_button_rect()
            panel_rect = self.get_panel_rect()

            if button_rect.collidepoint(event.pos):
                self.toggle()
                return

            if self.open:
                all_rect, normal_rect, fast_rect = self.get_filter_button_rects()

                if all_rect.collidepoint(event.pos):
                    self.active_filter = "all"
                    return

                if normal_rect.collidepoint(event.pos):
                    self.active_filter = "normal"
                    return

                if fast_rect.collidepoint(event.pos):
                    self.active_filter = "fast"
                    return

                if not panel_rect.collidepoint(event.pos):
                    self.toggle()

    def get_button_rect(self):
        return pygame.Rect(
            self.screen_width - self.button_w,
            self.screen_height // 2 - self.button_h // 2,
            self.button_w,
            self.button_h
        )

    def get_panel_rect(self):
        return pygame.Rect(int(self.x), 0, self.width, self.screen_height)

    def get_filter_button_rects(self):
        panel = self.get_panel_rect()

        btn_w = 110
        btn_h = 36
        gap = 10

        top_y = panel.y + 70
        start_x = panel.right - btn_w - 20

        all_rect = pygame.Rect(start_x, top_y, btn_w, btn_h)
        normal_rect = pygame.Rect(start_x, top_y + btn_h + gap, btn_w, btn_h)
        fast_rect = pygame.Rect(start_x, top_y + (btn_h + gap) * 2, btn_w, btn_h)

        return all_rect, normal_rect, fast_rect