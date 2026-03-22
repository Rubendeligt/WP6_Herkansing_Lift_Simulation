import pygame
import sys

from Python.Variables import MIN_FLOORS, MAX_FLOORS, make_buttons
from Python.simulation import Simulation
from Python.renderer import Renderer
from Python.Information import InformationPanel
from Python.Draw import draw_information_panel, draw_time


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
    info_panel = InformationPanel(width, height)

    btn_minus, btn_plus, btn_monitor = make_buttons(width)

    current_view = "simulation"
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        offset = max(0, info_panel.screen_width - info_panel.get_panel_rect().x)

        shifted_minus = btn_minus.move(-offset, 0)
        shifted_plus = btn_plus.move(-offset, 0)
        shifted_monitor = btn_monitor.move(-offset, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if current_view == "simulation":
                info_panel.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if shifted_monitor.collidepoint(mouse_pos):
                    current_view = "monitor" if current_view == "simulation" else "simulation"

                elif current_view == "simulation":
                    if shifted_minus.collidepoint(mouse_pos):
                        simulation.set_floors(max(MIN_FLOORS, simulation.floors - 1))

                    elif shifted_plus.collidepoint(mouse_pos):
                        simulation.set_floors(min(MAX_FLOORS, simulation.floors + 1))

        if current_view == "simulation":
            simulation.update(dt)
            info_panel.update(dt)

        renderer.draw(simulation, btn_minus, btn_plus, btn_monitor, current_view, offset)

        if current_view == "simulation":
            draw_information_panel(screen, info_panel, font, simulation)
            draw_time(screen, font, simulation)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()