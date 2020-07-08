import pygame, sys
from pygame.locals import *
from config import PLOTTER_WIDTH, PLOTTER_HEIGHT


def output_rectanges(completed_rectangles):
    output = []
    for left, top, width, height in completed_rectangles:
        top_line = [(left, top), (left + width, top)]
        bottom_line = [(left, top + height), (left + width, top + height)]
        left_line = [(left, top), (left, top + height)]
        right_line = [(left + width, top), (left + width, top + height)]
        output.append((top_line, bottom_line, left_line, right_line))
    return {"rectangles": output}


def main():
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    mouse_position = (0, 0)
    is_drawing = False
    screen = pygame.display.set_mode((PLOTTER_WIDTH, PLOTTER_HEIGHT), 0, 32)
    screen.fill(WHITE)
    pygame.display.set_caption("Python to Arduino")

    start_top = 0
    start_left = 0
    current_top = 0
    current_left = 0
    completed_rectangles = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:

                pygame.quit()
                return output_rectanges(completed_rectangles)
                # sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                is_drawing = True
                start_left, start_top = pygame.mouse.get_pos()
                current_left = start_left
                current_top = start_top
            elif event.type == MOUSEBUTTONUP:
                is_drawing = False
                completed_rectangles.append(
                    (
                        start_left,
                        start_top,
                        current_left - start_left,
                        current_top - start_top,
                    )
                )
            elif event.type == MOUSEMOTION:
                if is_drawing:
                    current_left, current_top = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.mod and pygame.K_LCTRL and event.key == pygame.K_z:
                    if len(completed_rectangles) > 0:
                        completed_rectangles.pop()

        screen.fill(WHITE)
        if is_drawing:
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    start_left,
                    start_top,
                    current_left - start_left,
                    current_top - start_top,
                ),
                3,
            )
        for rectangle in completed_rectangles:
            pygame.draw.rect(screen, BLACK, rectangle, 3)
        pygame.display.update()


if __name__ == "__main__":
    main()
