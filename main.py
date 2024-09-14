import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAMES_PER_SECOND = 30


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = pygame.Rect((300, 250, 50, 50))
clock = pygame.time.Clock()



run = True
while run:


    screen.fill((0,0,0))

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True :
        player.move_ip(-1,0)
    elif key[pygame.K_d] == True :
        player.move_ip(1,0)
    elif key[pygame.K_w] == True :
        player.move_ip(0, -1)
    elif key[pygame.K_s] == True :
        player.move_ip(0, 1)

    pygame.draw.rect(screen, (255,0,0), player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)



pygame.quit()