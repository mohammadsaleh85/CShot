import pygame
from sys import exit

height = 600
width = 1000

pygame.init()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,is_player1 = True):
        super(Player,self).__init__()
        self.is_player1 = is_player1
        self.surf = pygame.Surface((75,75))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        # Move player 1 
        if self.is_player1:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
        
        # Move player 2
        if self.is_player1 == False:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

#to create screen 
screen = pygame.display.set_mode((width,height))

#to create title for game
pygame.display.set_caption("cShot_E3")

#to set a background
background = pygame.image.load('aaa.png')
background = pygame.transform.scale(background,(width,height))

p1 = Player()
p2 = Player(False)
p2.surf.fill((0,0,0))
while True :
    #to exit from the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            exit()
    p1.move()
    p2.move()
    screen.blit(background,(0,0))
    screen.blit(p1.surf,p1.rect)
    screen.blit(p2.surf,p2.rect)
    #to update screen of game
    pygame.display.update()