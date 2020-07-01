import pygame

from config import *

pygame.init()
screen = pygame.display.set_mode((PLOTTER_WIDTH, PLOTTER_HEIGHT))
black = 0,0,0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    pygame.display.flip()