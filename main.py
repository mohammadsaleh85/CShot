import random
import pygame
from sys import exit

height = 600
width = 1000

pygame.init()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,is_player1 = True,init_num = 10,init_time = 60):
        super(Player,self).__init__()
        self.is_player1 = is_player1
        self.time = init_time
        self.surf = pygame.Surface((20,20))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.speed = 10
        self.bullet = []
        self.num = init_num

    def random_position(self):
        self.rect.x = random.randint(0,width)
        self.rect.y = random.randint(0,height)

    def shoot(self, event):
        if self.num > 0 and self.time > 0 and (
        (event.key == pygame.K_SPACE and self.is_player1 == False) or
        (event.key == pygame.K_RETURN and self.is_player1)):
            self.num -= 1
            self.bullet.append(Bullet(self.is_player1,self.rect.x,self.rect.y))
    
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

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player1, x, y):
        super(Bullet, self).__init__()
        self.is_player1 = is_player1
        self.radius = 10  # Radius of the bullet
        self.color = (255, 0, 0) if is_player1 else (0, 0, 255)  # Red for Player 1, Blue for Player 2
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)  # Define the bullet's bounding box
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)  # Draw the bullet as a circle

#to create screen 
screen = pygame.display.set_mode((width,height))

#to create title for game
pygame.display.set_caption("cShot_E3")

#to set a background
background = pygame.image.load('aaa.png')
background = pygame.transform.scale(background,(width,height))

# Create player
p1 = Player()
p2 = Player(is_player1=False)

# Set player random position
p1.random_position()
p2.random_position()

p2.surf.fill((0,0,0))

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            p1.shoot(event)
            p2.shoot(event)

    # Player actions
    p1.move()
    p2.move()

        # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(p1.surf, p1.rect)
    screen.blit(p2.surf, p2.rect)
    for bullet in p1.bullet:
        bullet.draw(screen)
    for bullet in p2.bullet:
        bullet.draw(screen)

    # Update the display
    pygame.display.update()