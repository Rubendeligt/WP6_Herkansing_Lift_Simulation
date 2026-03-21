import pygame

# m.b.v Stackoverflow
def draw_wait_time_graph(screen, panel_rect, font, simulation):
    history = simulation.get_wait_time_history()

    graph_margin_x = 20
    graph_margin_top = 280
    graph_width = panel_rect.width - 40
    graph_height = 180

    graph_rect = pygame.Rect(
        panel_rect.x + graph_margin_x,
        graph_margin_top,
        graph_width,
        graph_height
    )

    pygame.draw.rect(screen, (40, 40, 55), graph_rect, border_radius=8)
    pygame.draw.rect(screen, (120, 120, 140), graph_rect, 2, border_radius=8)

    title = font.render("Gem. wachttijd", True, (255, 255, 255))
    screen.blit(title, (graph_rect.x, graph_rect.y - 28))

    if len(history) < 2:
        no_data = font.render("Nog geen data", True, (180, 180, 180))
        screen.blit(no_data, (graph_rect.x + 10, graph_rect.y + 10))
        return

    times = [point[0] for point in history]
    waits = [point[1] for point in history]

    min_time = times[0]
    max_time = times[-1]
    max_wait = max(max(waits), 1)

    pygame.draw.line(
        screen,
        (180, 180, 180),
        (graph_rect.x + 35, graph_rect.bottom - 25),
        (graph_rect.right - 10, graph_rect.bottom - 25),
        2
    )
    pygame.draw.line(
        screen,
        (180, 180, 180),
        (graph_rect.x + 35, graph_rect.y + 10),
        (graph_rect.x + 35, graph_rect.bottom - 25),
        2
    )

    for i in range(5):
        value = max_wait * (4 - i) / 4
        y = graph_rect.y + 10 + i * ((graph_rect.height - 35) / 4)

        label = font.render(f"{value:.1f}", True, (180, 180, 180))
        screen.blit(label, (graph_rect.x, y - 8))

        pygame.draw.line(
            screen,
            (70, 70, 85),
            (graph_rect.x + 35, int(y)),
            (graph_rect.right - 10, int(y)),
            1
        )
    points = []
    usable_width = graph_rect.width - 45
    usable_height = graph_rect.height - 35

    for time_value, wait_value in history:
        if max_time == min_time:
            x = graph_rect.x + 35
        else:
            x = graph_rect.x + 35 + ((time_value - min_time) / (max_time - min_time)) * usable_width

        y = graph_rect.bottom - 25 - (wait_value / max_wait) * usable_height
        points.append((int(x), int(y)))

    if len(points) >= 2:
        pygame.draw.lines(screen, (80, 220, 120), False, points, 3)

    for point in points:
        pygame.draw.circle(screen, (255, 255, 255), point, 3)

    start_label = _minutes_to_string(min_time)
    end_label = _minutes_to_string(max_time)

    start_text = font.render(start_label, True, (180, 180, 180))
    end_text = font.render(end_label, True, (180, 180, 180))

    screen.blit(start_text, (graph_rect.x + 35, graph_rect.bottom - 20))
    screen.blit(end_text, (graph_rect.right - end_text.get_width() - 10, graph_rect.bottom - 20))

def draw_people_graph(screen, panel_rect, font, simulation):
    history = simulation.get_people_history()

    graph_margin_x = 20
    graph_margin_top = 500
    graph_width = panel_rect.width - 40
    graph_height = 180

    graph_rect = pygame.Rect(
        panel_rect.x + graph_margin_x,
        graph_margin_top,
        graph_width,
        graph_height
    )

    pygame.draw.rect(screen, (40, 40, 55), graph_rect, border_radius=8)
    pygame.draw.rect(screen, (120, 120, 140), graph_rect, 2, border_radius=8)

    title = font.render("Aantal mensen", True, (255, 255, 255))
    screen.blit(title, (graph_rect.x, graph_rect.y - 28))

    if len(history) < 2:
        no_data = font.render("Nog geen data", True, (180, 180, 180))
        screen.blit(no_data, (graph_rect.x + 10, graph_rect.y + 10))
        return

    times = [point[0] for point in history]
    people_counts = [point[1] for point in history]

    min_time = times[0]
    max_time = times[-1]
    max_people = max(max(people_counts), 1)

    pygame.draw.line(
        screen,
        (180, 180, 180),
        (graph_rect.x + 35, graph_rect.bottom - 25),
        (graph_rect.right - 10, graph_rect.bottom - 25),
        2
    )
    pygame.draw.line(
        screen,
        (180, 180, 180),
        (graph_rect.x + 35, graph_rect.y + 10),
        (graph_rect.x + 35, graph_rect.bottom - 25),
        2
    )

    for i in range(5):
        value = max_people * (4 - i) / 4
        y = graph_rect.y + 10 + i * ((graph_rect.height - 35) / 4)

        label = font.render(f"{int(value)}", True, (180, 180, 180))
        screen.blit(label, (graph_rect.x, y - 8))

        pygame.draw.line(
            screen,
            (70, 70, 85),
            (graph_rect.x + 35, int(y)),
            (graph_rect.right - 10, int(y)),
            1
        )

    points = []
    usable_width = graph_rect.width - 45
    usable_height = graph_rect.height - 35

    for time_value, people_value in history:
        if max_time == min_time:
            x = graph_rect.x + 35
        else:
            x = graph_rect.x + 35 + ((time_value - min_time) / (max_time - min_time)) * usable_width

        y = graph_rect.bottom - 25 - (people_value / max_people) * usable_height
        points.append((int(x), int(y)))

    if len(points) >= 2:
        pygame.draw.lines(screen, (90, 170, 255), False, points, 3)

    for point in points:
        pygame.draw.circle(screen, (255, 255, 255), point, 3)

    start_label = _minutes_to_string(min_time)
    end_label = _minutes_to_string(max_time)

    start_text = font.render(start_label, True, (180, 180, 180))
    end_text = font.render(end_label, True, (180, 180, 180))

    screen.blit(start_text, (graph_rect.x + 35, graph_rect.bottom - 20))
    screen.blit(end_text, (graph_rect.right - end_text.get_width() - 10, graph_rect.bottom - 20))

def _minutes_to_string(total_minutes):
    total_minutes = int(total_minutes)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"