import pygame
import sys

from Python.Variables import MIN_FLOORS, MAX_FLOORS, make_buttons
from Python.simulation import Simulation
from Python.renderer import Renderer
from Python.Information import InformationPanel
from Python.Draw import draw_information_panel, draw_time
from Python.Drukte import (DruktePanel, draw_drukte_panel, handle_drukte_click, get_drukte_buttons,)


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
    drukte_panel = DruktePanel(width, height)

    btn_minus, btn_plus, btn_monitor, btn_add_normal_lift, btn_add_fast_lift, btn_remove_lift = make_buttons(width)

    current_view = "simulation"
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        offset = max(0, info_panel.screen_width - info_panel.get_panel_rect().x)

        shifted_minus = btn_minus.move(-offset, 0)
        shifted_plus = btn_plus.move(-offset, 0)
        shifted_monitor = btn_monitor.move(-offset, 0)
        shifted_add_normal_lift = btn_add_normal_lift.move(-offset, 0)
        shifted_add_fast_lift = btn_add_fast_lift.move(-offset, 0)
        shifted_remove_lift = btn_remove_lift.move(-offset, 0)

        drukte_buttons = []
        if current_view == "simulation" and drukte_panel.get_panel_rect().x < drukte_panel.screen_width:
            drukte_buttons = get_drukte_buttons(simulation, drukte_panel)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if current_view == "simulation":
                info_panel.handle_event(event)
                drukte_panel.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if shifted_monitor.collidepoint(mouse_pos):
                    current_view = "monitor" if current_view == "simulation" else "simulation"

                elif current_view == "simulation":
                    if shifted_minus.collidepoint(mouse_pos):
                        simulation.set_floors(max(MIN_FLOORS, simulation.floors - 1))

                    elif shifted_plus.collidepoint(mouse_pos):
                        simulation.set_floors(min(MAX_FLOORS, simulation.floors + 1))

                    elif shifted_add_normal_lift.collidepoint(mouse_pos):
                        simulation.add_lift("normal")

                    elif shifted_add_fast_lift.collidepoint(mouse_pos):
                        simulation.add_lift("fast")

                    elif shifted_remove_lift.collidepoint(mouse_pos):
                        simulation.remove_last_lift()

                    else:
                        handle_drukte_click(mouse_pos, simulation, drukte_buttons)

                elif current_view == "monitor":
                    for rect, idx in renderer.button_rects:
                        if rect.collidepoint(mouse_pos):
                            renderer.selected_lift = idx

                    if renderer.stop_rect and renderer.stop_rect.collidepoint(mouse_pos):
                        renderer.stop_active = not renderer.stop_active

                    if renderer.call_rect and renderer.call_rect.collidepoint(mouse_pos):
                        renderer.call_active = not renderer.call_active

                        if renderer.call_active:
                            renderer.small_lift_targets[renderer.selected_lift] = 0.10
                        else:
                            renderer.small_lift_targets[renderer.selected_lift] = 0.45

        if current_view == "simulation":
            simulation.update(dt)
            info_panel.update(dt)
            drukte_panel.update(dt)

        renderer.update_animations(dt)

        renderer.draw(
            simulation,
            btn_minus,
            btn_plus,
            btn_monitor,
            btn_add_normal_lift,
            btn_add_fast_lift,
            btn_remove_lift,
            current_view,
            offset
        )

        if current_view == "simulation":
            draw_information_panel(screen, info_panel, font, simulation)
            draw_time(screen, font, simulation)
            draw_drukte_panel(screen, font, simulation, drukte_panel)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()