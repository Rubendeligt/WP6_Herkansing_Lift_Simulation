import pygame
import Python.People as PeopleModule
from Python.Draw import draw_building, draw_button
from Python.Lift import draw_lift


class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.draw_people = PeopleModule.draw_people

    def draw(self, simulation, btn_minus, btn_plus, btn_monitor, current_view, offset=0):
        if current_view == "simulation":
            self.draw_simulation(simulation, btn_minus, btn_plus, btn_monitor, offset)
        else:
            self.draw_monitor(btn_monitor)

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
        draw_button(self.screen, self.font, shifted_monitor, "tweede screen")

    def draw_monitor(self, btn_monitor, offset=0):
        self.screen.fill((30, 30, 30))

        shifted_monitor = btn_monitor.move(-offset, 0)
        draw_button(self.screen, self.font, shifted_monitor, "Back")

        text = self.font.render("Monitor Screen", True, (255, 255, 255))
        self.screen.blit(text, (40, 40))

        pygame.display.flip()