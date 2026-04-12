import pygame
import sys

from Python.Setting_sidebar import SettingSidebar, draw_Setting_sidebar
from Python.Variables import MIN_FLOORS, MAX_FLOORS, make_buttons
from Python.simulation import Simulation
from Python.renderer import Renderer
from Python.Information import InformationPanel
from Python.Draw import draw_information_panel, draw_time, draw_button
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
    setting_sidebar = SettingSidebar(width, height)
    _, _, btn_monitor, _, _, _ = make_buttons(width)
    btn_monitor.width = 140
    btn_monitor.height = 60
    btn_monitor.bottomright = (width - 20, height - 20)

    current_view = "simulation"
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        offset = max(0, info_panel.screen_width - info_panel.get_panel_rect().x)

        (
            btn_minus,
            btn_plus,
            btn_add_normal_lift,
            btn_add_fast_lift,
            btn_remove_lift,
            btn_restart_day,
        ) = setting_sidebar.get_button_rects()
        info_open = info_panel.get_panel_rect().x < info_panel.screen_width
        drukte_open = drukte_panel.get_panel_rect().x < drukte_panel.screen_width
        setting_open = setting_sidebar.get_panel_rect().x < setting_sidebar.screen_width

        drukte_buttons = []
        if current_view == "simulation" and drukte_open:
            drukte_buttons = get_drukte_buttons(simulation, drukte_panel)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if current_view == "simulation":
                if info_open:
                    info_panel.handle_event(event)
                elif drukte_open:
                    drukte_panel.handle_event(event)
                elif setting_open:
                    setting_sidebar.handle_event(event)
                else:
                    info_panel.handle_event(event)
                    drukte_panel.handle_event(event)
                    setting_sidebar.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if btn_monitor.collidepoint(mouse_pos):
                    current_view = "monitor" if current_view == "simulation" else "simulation"

                elif current_view == "simulation":
                    if btn_minus.collidepoint(mouse_pos):
                        simulation.set_floors(max(MIN_FLOORS, simulation.floors - 1))

                    elif btn_plus.collidepoint(mouse_pos):
                        simulation.set_floors(min(MAX_FLOORS, simulation.floors + 1))

                    elif btn_add_normal_lift.collidepoint(mouse_pos):
                        simulation.add_lift("normal")

                    elif btn_add_fast_lift.collidepoint(mouse_pos):
                        simulation.add_lift("fast")

                    elif btn_remove_lift.collidepoint(mouse_pos):
                        simulation.remove_last_lift()

                    elif btn_restart_day.collidepoint(mouse_pos):
                        simulation = Simulation(width, height, floors=simulation.floors)

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
            if not info_open and not drukte_open:
                setting_sidebar.update(dt)

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
            0
        )

        if current_view == "simulation":
            draw_information_panel(screen, info_panel, font, simulation)
            draw_time(screen, font, simulation)
            draw_drukte_panel(screen, font, simulation, drukte_panel)
            if not info_open and not drukte_open:
                draw_Setting_sidebar(screen, font, setting_sidebar)
            draw_button(screen, font, btn_minus, "verdieping minder")
            draw_button(screen, font, btn_plus, "verdieping meer")
            draw_button(screen, font, btn_add_normal_lift, "+ normale lift")
            draw_button(screen, font, btn_add_fast_lift, "+ snelle lift")
            draw_button(screen, font, btn_remove_lift, "lift verwijderen")
            draw_button(screen, font, btn_restart_day, "dag herstarten")
            draw_button(screen, font, btn_monitor, "tweede scherm")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()