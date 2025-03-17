import pygame

pygame.init()

screen_of_menu = pygame.display.set_mode((600,300))

run = True

while run : 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT :
            run = False

    pygame.display.update()
pygame.quit()