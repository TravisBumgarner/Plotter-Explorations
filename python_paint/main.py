import pygame, sys
from pygame.locals import *
from config import PLOTTER_WIDTH, PLOTTER_HEIGHT

def main():
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    mouse_position = (0, 0)
    is_drawing = False
    screen = pygame.display.set_mode((PLOTTER_WIDTH, PLOTTER_HEIGHT), 0, 32)
    screen.fill(WHITE)
    pygame.display.set_caption("Python to Arduino")

    last_position = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                is_drawing = True
            elif event.type == MOUSEBUTTONUP:
                mouse_position = (0, 0)
                is_drawing = False
                last_position = None
            elif event.type == MOUSEMOTION:
                if (is_drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_position is not None:
                        pygame.draw.line(screen, BLACK, last_position, mouse_position, 1)
                    last_position = mouse_position

        pygame.display.update()

if __name__ == "__main__":
    main()