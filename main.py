#import
import pygame
from sys import exit

pygame.init()

#to create screen 
screen = pygame.display.set_mode((1280 , 720))

#to create title for game
pygame.display.set_caption("cShot_E3")

#to set a background
background = pygame.image.load('aaa.png')
background = pygame.transform.scale(background,(1280,720))



while True :
    #to exit from the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            exit()
    screen.blit(background,(0,0))
    #to update screen of game
    pygame.display.update()