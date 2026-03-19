import pygame
import sys

from Python.Variables import (
    MIN_FLOORS,
    MAX_FLOORS,
    make_buttons,
)
from Python.simulation import Simulation
from Python.renderer import Renderer


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("Lift Simulator")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18)

    simulation = Simulation(width, height, floors=6)
    renderer = Renderer(screen, font)

    btn_minus, btn_plus = make_buttons(width)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if btn_minus.collidepoint(mouse_pos):
                    simulation.set_floors(max(MIN_FLOORS, simulation.floors - 1))

                if btn_plus.collidepoint(mouse_pos):
                    simulation.set_floors(min(MAX_FLOORS, simulation.floors + 1))

        simulation.update(dt)
        renderer.draw(simulation, btn_minus, btn_plus)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()