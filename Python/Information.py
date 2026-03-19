import pygame


class InformationPanel:
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height

        self.width = 260
        self.button_w = 35
        self.button_h = 120

        self.open = False
        self.speed = 800

        self.x = width
        self.target_x = width

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
            if self.get_button_rect().collidepoint(event.pos):
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