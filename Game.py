import pygame
import sys

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Lift Simulator")

    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("arial", 18)

    FLOORS = 10
    TOP_MARGIN = 50
    BOTTOM_MARGIN = 50
    BUILDING_HEIGHT = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    FLOOR_HEIGHT = BUILDING_HEIGHT / FLOORS

    LEFT_MARGIN = 100
    RIGHT_MARGIN = 700

    WHITE = (255, 255, 255)
    BLACK = (20, 20, 20)
    GRAY = (120, 120, 120)

    def draw_building():
        """
        en toont het verdiepingsnummer.
        """
        for floor in range(FLOORS):
            y = TOP_MARGIN + floor * FLOOR_HEIGHT

            pygame.draw.line(screen, GRAY, (LEFT_MARGIN, y), (RIGHT_MARGIN, y), 2)
            label = FONT.render(f"Floor {FLOORS - floor - 1}", True, WHITE)
            screen.blit(label, (20, y - 10))


    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill(BLACK)

            draw_building()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()