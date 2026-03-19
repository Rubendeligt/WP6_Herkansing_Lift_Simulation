import pygame
import Python.People as PeopleModule
from Python.Draw import draw_building, draw_button
from Python.Lift import draw_lift


class Renderer:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.draw_people = PeopleModule.draw_people

    def draw(self, simulation, btn_minus: pygame.Rect, btn_plus: pygame.Rect) -> None:
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
        draw_button(self.screen, self.font, btn_minus, "–")
        draw_button(self.screen, self.font, btn_plus, "+")

        pygame.display.flip()