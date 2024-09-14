import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAMES_PER_SECOND = 60

pygame.display.set_caption('hot potato')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()




while True:


    screen.fill((0,0,0))

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)



