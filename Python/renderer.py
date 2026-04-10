import pygame
import Python.People as PeopleModule
from Python.Draw import draw_building, draw_button
from Python.Lift import draw_lift
from Python.Lifthover import draw_lift_hover_info


class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.draw_people = PeopleModule.draw_people
        self.hovered_lift_id = None
        self.hovered_lift_rect = None

        self.selected_lift = 0
        self.button_rects = []

        self.stop_rect = None
        self.call_rect = None
        self.stop_active = False
        self.call_active = False

        self.big_lift_number = "1"

        self.small_lift_positions = [0.45, 0.45, 0.45, 0.45]
        self.small_lift_targets = [0.45, 0.45, 0.45, 0.45]
        self.small_lift_speed = 0.8

    def draw(self, simulation, btn_minus, btn_plus, btn_monitor, btn_add_normal_lift, btn_add_fast_lift, btn_remove_lift, current_view, offset=0):
        if current_view == "simulation":
            self.draw_simulation(
                simulation,
                btn_minus,
                btn_plus,
                btn_monitor,
                btn_add_normal_lift,
                btn_add_fast_lift,
                btn_remove_lift,
                offset
            )
        else:
            self.draw_monitor(simulation, btn_monitor, offset)

    def update_animations(self, dt):
        for i in range(len(self.small_lift_positions)):
            current = self.small_lift_positions[i]
            target = self.small_lift_targets[i]

            if current < target:
                current += self.small_lift_speed * dt
                if current > target:
                    current = target
            elif current > target:
                current -= self.small_lift_speed * dt
                if current < target:
                    current = target

            self.small_lift_positions[i] = current

    def _ensure_small_lift_arrays(self, count):
        while len(self.small_lift_positions) < count:
            self.small_lift_positions.append(0.45)
            self.small_lift_targets.append(0.45)

        if len(self.small_lift_positions) > count:
            self.small_lift_positions = self.small_lift_positions[:count]
            self.small_lift_targets = self.small_lift_targets[:count]

    def draw_simulation(self, simulation, btn_minus, btn_plus, btn_monitor, btn_add_normal_lift, btn_add_fast_lift, btn_remove_lift, offset=0):
        self.screen.fill((230, 230, 230))

        draw_building(
            self.screen,
            self.font,
            simulation.floors,
            simulation.height,
            simulation.shaft_positions,
            simulation.shaft_w
        )

        mouse_pos = pygame.mouse.get_pos()
        self.hovered_lift_id = None
        self.hovered_lift_rect = None

        for lift in simulation.lifts:
            passenger_count = simulation.get_passenger_count(lift["id"])

            cab_rect = draw_lift(
                self.screen,
                lift["shaft_x"],
                lift["shaft_w"],
                lift["lift_w"],
                lift["lift_h"],
                lift["floor_pos"],
                simulation.floors,
                simulation.height,
                passenger_count,
                self.font,
                lift["type"]
            )

            if cab_rect.collidepoint(mouse_pos):
                self.hovered_lift_id = lift["id"]
                self.hovered_lift_rect = cab_rect

        self.draw_people(self.screen, simulation.people)

        draw_lift_hover_info(
            self.screen,
            self.font,
            simulation,
            self.hovered_lift_id,
            self.hovered_lift_rect
        )

    def draw_monitor(self, simulation, btn_monitor, offset=0):
        self.screen.fill((228, 230, 220))

        shifted_monitor = btn_monitor.move(-offset, 0)
        draw_button(self.screen, self.font, shifted_monitor, "Back")

        total_lifts = len(simulation.lifts)
        self._ensure_small_lift_arrays(max(total_lifts, 4))

        if total_lifts == 0:
            title_bar = pygame.Rect(0, 0, self.screen.get_width(), 50)
            pygame.draw.rect(self.screen, (70, 92, 170), title_bar)

            title = self.font.render("Lift Monitor", True, (255, 255, 255))
            self.screen.blit(title, (20, 15))
            return

        if self.selected_lift >= total_lifts:
            self.selected_lift = total_lifts - 1
        if self.selected_lift < 0:
            self.selected_lift = 0

        title_bar = pygame.Rect(0, 0, self.screen.get_width(), 50)
        pygame.draw.rect(self.screen, (70, 92, 170), title_bar)

        title = self.font.render("Lift Monitor", True, (255, 255, 255))
        self.screen.blit(title, (20, 15))

        left_margin = 80
        top_margin = 90
        area_width = self.screen.get_width() - 160
        area_height = self.screen.get_height() - 140

        section_height = area_height / 4
        shown_lifts = min(4, total_lifts)

        for i in range(shown_lifts):
            section_rect = pygame.Rect(
                left_margin,
                int(top_margin + i * section_height),
                int(area_width * 0.55),
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
                int(shaft_rect.y + shaft_rect.height * self.small_lift_positions[i]),
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

        center_x = int(self.screen.get_width() * 0.50)
        center_y = self.screen.get_height() // 2
        self._draw_center_panel(total_lifts, center_x, center_y)
        self._draw_big_lift_display(simulation)

    def _draw_center_panel(self, total_lifts, panel_center_x, panel_center_y):
        box_height = 160 if total_lifts <= 4 else 210
        box = pygame.Rect(panel_center_x - 80, panel_center_y - box_height // 2, 160, box_height)

        pygame.draw.rect(self.screen, (220, 220, 230), box)
        pygame.draw.rect(self.screen, (80, 80, 80), box, 2)

        title = self.font.render("H Rotterdam", True, (20, 20, 20))
        self.screen.blit(title, (box.x + 10, box.y + 10))

        self.button_rects.clear()

        max_buttons = min(total_lifts, 4)
        button_defs = [
            (box.x + 15, box.y + 40),
            (box.x + 65, box.y + 40),
            (box.x + 15, box.y + 75),
            (box.x + 65, box.y + 75),
        ]

        for idx in range(max_buttons):
            x, y = button_defs[idx]
            r = pygame.Rect(x, y, 30, 30)

            if self.selected_lift == idx:
                color = (100, 160, 255)
            else:
                color = (240, 240, 250)

            pygame.draw.rect(self.screen, color, r)
            pygame.draw.rect(self.screen, (90, 90, 90), r, 1)

            t = self.font.render(str(idx + 1), True, (20, 20, 20))
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

    def _draw_big_lift_display(self, simulation):
        total_lifts = len(simulation.lifts)
        if total_lifts == 0:
            return

        if self.selected_lift >= total_lifts:
            self.selected_lift = total_lifts - 1

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        lift = simulation.lifts[self.selected_lift]

        area_x = int(screen_w * 0.68)
        area_y = 120
        area_w = int(screen_w * 0.22)
        area_h = int(screen_h * 0.50)

        frame1 = pygame.Rect(area_x, area_y, area_w, area_h)
        frame2 = pygame.Rect(area_x + 16, area_y + 16, area_w - 32, area_h - 32)
        frame3 = pygame.Rect(area_x + 32, area_y + 32, area_w - 64, area_h - 64)
        inner = pygame.Rect(area_x + 50, area_y + 50, area_w - 100, area_h - 100)

        if self.selected_lift == 0:
            frame1_color = (0, 235, 255)
            frame2_color = (0, 120, 255)
            frame3_color = (70, 70, 255)
            bottom_color = (255, 0, 220)
        elif self.selected_lift == 1:
            frame1_color = (255, 220, 0)
            frame2_color = (255, 150, 0)
            frame3_color = (220, 90, 0)
            bottom_color = (255, 80, 80)
        else:
            frame1_color = (255, 170, 220)
            frame2_color = (220, 100, 180)
            frame3_color = (150, 60, 140)
            bottom_color = (120, 60, 180)

        pygame.draw.rect(self.screen, frame1_color, frame1)
        pygame.draw.rect(self.screen, frame2_color, frame2)
        pygame.draw.rect(self.screen, frame3_color, frame3)
        pygame.draw.rect(self.screen, (245, 245, 245), inner)

        bottom_bar = pygame.Rect(frame1.x, frame1.bottom - 14, frame1.width, 14)
        pygame.draw.rect(self.screen, bottom_color, bottom_bar)

        for i in range(4):
            cx = frame3.x + 22 + i * 18
            cy = frame3.y - 8
            pygame.draw.circle(self.screen, (190, 200, 220), (cx, cy), 6)
            pygame.draw.circle(self.screen, (70, 70, 70), (cx, cy), 6, 1)

        cabin_area = inner.inflate(-20, -20)
        pygame.draw.rect(self.screen, (225, 225, 230), cabin_area)

        door_gap = int(cabin_area.width * 0.28) if self.call_active else 0
        half_width = cabin_area.width // 2

        left_door = pygame.Rect(
            cabin_area.x,
            cabin_area.y,
            half_width - door_gap // 2,
            cabin_area.height
        )

        right_door = pygame.Rect(
            cabin_area.centerx + door_gap // 2,
            cabin_area.y,
            half_width - door_gap // 2,
            cabin_area.height
        )

        door_color = (210, 210, 218)
        door_border = (110, 110, 120)

        pygame.draw.rect(self.screen, door_color, left_door)
        pygame.draw.rect(self.screen, door_border, left_door, 2)

        pygame.draw.rect(self.screen, door_color, right_door)
        pygame.draw.rect(self.screen, door_border, right_door, 2)

        if left_door.width > 8:
            pygame.draw.line(
                self.screen,
                (90, 90, 100),
                (left_door.right - 6, left_door.y + 15),
                (left_door.right - 6, left_door.bottom - 15),
                2
            )

        if right_door.width > 8:
            pygame.draw.line(
                self.screen,
                (90, 90, 100),
                (right_door.x + 6, right_door.y + 15),
                (right_door.x + 6, right_door.bottom - 15),
                2
            )

        big_font_size = max(36, inner.height // 2)
        big_font = pygame.font.SysFont("arial", big_font_size, bold=True)

        number_text = big_font.render(str(self.selected_lift + 1), True, (40, 40, 70))
        self.screen.blit(number_text, number_text.get_rect(center=inner.center))

        side_panel = pygame.Rect(inner.x - 22, inner.y + 25, 16, 52)
        pygame.draw.rect(self.screen, (220, 220, 220), side_panel)
        pygame.draw.rect(self.screen, (90, 90, 90), side_panel, 1)

        for i in range(4):
            pygame.draw.circle(
                self.screen,
                frame2_color,
                (side_panel.x + 8, side_panel.y + 8 + i * 11),
                3
            )

        info_y = frame1.bottom + 70
        type_text = self.font.render(f"Type: {lift['type']}", True, (30, 30, 30))
        floor_text = self.font.render(f"Floor: {lift['floor'] + 1}", True, (30, 30, 30))
        passengers = simulation.get_passenger_count(lift["id"])
        people_text = self.font.render(f"People: {passengers}", True, (30, 30, 30))

        self.screen.blit(type_text, (frame1.x, info_y))
        self.screen.blit(floor_text, (frame1.x, info_y + 28))
        self.screen.blit(people_text, (frame1.x, info_y + 56))

        self._draw_door_status_indicator(frame1)

    def _draw_door_status_indicator(self, frame1):
        status_box = pygame.Rect(frame1.x, frame1.y + frame1.height + 18, frame1.width, 42)
        pygame.draw.rect(self.screen, (215, 218, 225), status_box)
        pygame.draw.rect(self.screen, (90, 90, 100), status_box, 2)

        if self.stop_active:
            indicator_color = (230, 70, 70)
            status_text = "STOP"
            detail_text = "Lift paused"
        elif self.call_active:
            indicator_color = (80, 210, 120)
            status_text = "OPEN"
            detail_text = "Door open"
        else:
            indicator_color = (160, 160, 170)
            status_text = "CLOSED"
            detail_text = "Door closed"

        indicator_rect = pygame.Rect(status_box.x + 14, status_box.y + 10, 22, 22)
        pygame.draw.ellipse(self.screen, indicator_color, indicator_rect)
        pygame.draw.ellipse(self.screen, (70, 70, 70), indicator_rect, 1)

        label = self.font.render(status_text, True, (30, 30, 30))
        self.screen.blit(label, (indicator_rect.right + 12, status_box.y + 5))

        small_font = pygame.font.SysFont("arial", 14)
        detail = small_font.render(detail_text, True, (70, 70, 70))
        self.screen.blit(detail, (indicator_rect.right + 12, status_box.y + 22))