#import
import pygame
from sys import exit

pygame.init()

#to create screen 
screen = pygame.display.set_mode((1280 , 720))

while True :
    #to exit from the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            exit()
    
    #to update screen of game
    pygame.display.update()