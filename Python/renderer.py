import pygame
import Python.People as PeopleModule
from Python.Draw import draw_building, draw_button
from Python.Lift import draw_lift


class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.draw_people = PeopleModule.draw_people

        self.selected_lift = 0
        self.button_rects = []

        self.stop_rect = None
        self.call_rect = None
        self.stop_active = False
        self.call_active = False

    def draw(self, simulation, btn_minus, btn_plus, btn_monitor, current_view, offset=0):
        if current_view == "simulation":
            self.draw_simulation(simulation, btn_minus, btn_plus, btn_monitor, offset)
        else:
            self.draw_monitor(btn_monitor, offset)

    def draw_simulation(self, simulation, btn_minus, btn_plus, btn_monitor, offset=0):
        self.screen.fill((230, 230, 230))

        draw_building(
            self.screen,
            self.font,
            simulation.floors,
            simulation.height,
            simulation.shaft_positions,
            simulation.shaft_w
        )

        for lift in simulation.lifts:
            passenger_count = simulation.get_passenger_count(lift["id"])

            draw_lift(
                self.screen,
                lift["shaft_x"],
                lift["shaft_w"],
                lift["lift_w"],
                lift["lift_h"],
                lift["floor_pos"],
                simulation.floors,
                simulation.height,
                passenger_count,
                self.font
            )

        self.draw_people(self.screen, simulation.people)

        shifted_minus = btn_minus.move(-offset, 0)
        shifted_plus = btn_plus.move(-offset, 0)
        shifted_monitor = btn_monitor.move(-offset, 0)

        draw_button(self.screen, self.font, shifted_minus, "-")
        draw_button(self.screen, self.font, shifted_plus, "+")
        draw_button(self.screen, self.font, shifted_monitor, "tweede scherm")

    def draw_monitor(self, btn_monitor, offset=0):
        self.screen.fill((228, 230, 220))

        shifted_monitor = btn_monitor.move(-offset, 0)
        draw_button(self.screen, self.font, shifted_monitor, "Back")

        title_bar = pygame.Rect(0, 0, self.screen.get_width(), 50)
        pygame.draw.rect(self.screen, (70, 92, 170), title_bar)

        title = self.font.render("Lift Monitor", True, (255, 255, 255))
        self.screen.blit(title, (20, 15))

        left_margin = 80
        top_margin = 90
        area_width = self.screen.get_width() - 160
        area_height = self.screen.get_height() - 140

        section_height = area_height / 4

        for i in range(4):
            section_rect = pygame.Rect(
                left_margin,
                int(top_margin + i * section_height),
                area_width,
                int(section_height - 15)
            )

            if self.selected_lift == i:
                section_color = (195, 215, 255)
                border_color = (60, 100, 190)
            else:
                section_color = (210, 214, 222)
                border_color = (80, 84, 92)

            pygame.draw.rect(self.screen, section_color, section_rect)
            pygame.draw.rect(self.screen, border_color, section_rect, 2)

            shaft_rect = pygame.Rect(
                section_rect.x + 25,
                section_rect.y + 18,
                int(section_rect.width * 0.18),
                int(section_rect.height * 0.55)
            )

            pygame.draw.rect(self.screen, (186, 196, 220), shaft_rect)
            pygame.draw.rect(self.screen, (70, 90, 130), shaft_rect, 2)

            for stripe_x in range(int(shaft_rect.x + 6), int(shaft_rect.right - 2), 10):
                pygame.draw.line(
                    self.screen,
                    (150, 170, 210),
                    (stripe_x, shaft_rect.y + 3),
                    (stripe_x, shaft_rect.bottom - 3),
                    2
                )

            cab_rect = pygame.Rect(
                shaft_rect.x + 6,
                int(shaft_rect.y + shaft_rect.height * (0.15 if i == 0 else 0.45)),
                shaft_rect.width - 12,
                int(shaft_rect.height * 0.28)
            )

            pygame.draw.rect(self.screen, (72, 118, 210), cab_rect)
            pygame.draw.rect(
                self.screen,
                (255, 90, 170),
                (cab_rect.x, cab_rect.bottom - 4, cab_rect.width, 4)
            )

            text_x = shaft_rect.right + 40
            text_y = section_rect.y + 25

            label = self.font.render(f"Lift {i + 1}", True, (30, 30, 30))
            self.screen.blit(label, (text_x, text_y))

            floor_text = self.font.render("Floor: --", True, (60, 60, 60))
            self.screen.blit(floor_text, (text_x, text_y + 30))

            pygame.draw.circle(self.screen, (170, 176, 190), (text_x + 10, text_y + 70), 8)
            pygame.draw.circle(self.screen, (90, 96, 110), (text_x + 10, text_y + 70), 8, 1)

            pygame.draw.circle(self.screen, (170, 176, 190), (text_x + 35, text_y + 70), 8)
            pygame.draw.circle(self.screen, (90, 96, 110), (text_x + 35, text_y + 70), 8, 1)

        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self._draw_center_panel(center_x, center_y)

    def _draw_center_panel(self, panel_center_x, panel_center_y):
        box = pygame.Rect(panel_center_x - 60, panel_center_y - 80, 120, 160)

        pygame.draw.rect(self.screen, (220, 220, 230), box)
        pygame.draw.rect(self.screen, (80, 80, 80), box, 2)

        title = self.font.render("WornVator", True, (20, 20, 20))
        self.screen.blit(title, (box.x + 10, box.y + 10))

        self.button_rects.clear()

        buttons = [
            ("1", box.x + 15, box.y + 40, 0),
            ("2", box.x + 65, box.y + 40, 1),
            ("3", box.x + 15, box.y + 75, 2),
            ("4", box.x + 65, box.y + 75, 3),
        ]

        for text, x, y, idx in buttons:
            r = pygame.Rect(x, y, 30, 30)

            if self.selected_lift == idx:
                color = (100, 160, 255)
            else:
                color = (240, 240, 250)

            pygame.draw.rect(self.screen, color, r)
            pygame.draw.rect(self.screen, (90, 90, 90), r, 1)

            t = self.font.render(text, True, (20, 20, 20))
            self.screen.blit(t, t.get_rect(center=r.center))

            self.button_rects.append((r, idx))

        self.stop_rect = pygame.Rect(box.x + 15, box.y + 115, 40, 20)
        self.call_rect = pygame.Rect(box.x + 65, box.y + 115, 40, 20)

        stop_color = (255, 80, 80) if self.stop_active else (220, 60, 60)
        call_color = (120, 180, 255) if self.call_active else (210, 215, 245)

        pygame.draw.rect(self.screen, stop_color, self.stop_rect)
        pygame.draw.rect(self.screen, (120, 20, 20), self.stop_rect, 1)

        pygame.draw.rect(self.screen, call_color, self.call_rect)
        pygame.draw.rect(self.screen, (60, 60, 100), self.call_rect, 1)

        stop_text = self.font.render("STOP", True, (255, 255, 255))
        call_text = self.font.render("CALL", True, (20, 20, 20))

        self.screen.blit(stop_text, stop_text.get_rect(center=self.stop_rect.center))
        self.screen.blit(call_text, call_text.get_rect(center=self.call_rect.center))