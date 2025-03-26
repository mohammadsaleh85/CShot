import random
import pygame
import sys
from pygame import mixer


height = 600
width = 1000

# Get usernames from command-line arguments
print(sys.argv)
if len(sys.argv) > 2:
    username1 = sys.argv[1]
    username2 = sys.argv[2]
else:
    username1 = "Player 1"
    username2 = "Player 2"

pygame.init()
mixer.init()

bullet_sound = mixer.Sound('arrow_s.mp3')
score_sound = mixer.Sound('success.mp3')
tictac = mixer.Sound('tictac.mp3')
empty_shot = mixer.Sound('empty_shot.mp3')

mixer.music.load('game_sound.mp3')
mixer.music.set_volume(0.3)
mixer.music.play()



# initialize the font
font = pygame.font.Font('slkscre.ttf', 20)  # Font for displaying time
# intialize the clock
clock = pygame.time.Clock()  # Clock to control the frame rate

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,is_player1 = True,init_num = 10,init_time = 60):
        super(Player,self).__init__()
        self.is_player1 = is_player1
        self.time = init_time
        self.surf = pygame.Surface((15,15))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.speed = 8
        self.num = init_num
        self.score = 0

    def random_position(self):
        self.rect.x = random.randint(0,width)
        self.rect.y = random.randint(0,height)

    def shoot(self, event):
        if self.num > 0 and self.time > 0 and (
        (event.key == pygame.K_SPACE and self.is_player1 == False) or
        (event.key == pygame.K_RETURN and self.is_player1)):
            self.num -= 1
            bullet_sound.play()
            all_sprites.add(Bullet(self.is_player1,self.rect.x,self.rect.y))
            bullets.add(Bullet(self.is_player1,self.rect.x,self.rect.y))
        if self.num == 0 and self.time > 0 and (
        (event.key == pygame.K_SPACE and self.is_player1 == False) or
        (event.key == pygame.K_RETURN and self.is_player1)):
            empty_shot.play()
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
        self.radius = 7  # Radius of the bullet
        self.color = "yellow" if is_player1 else "red"  # Red for Player 1, Blue for Player 2
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)  # Define the bullet's bounding box
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)  # Draw the bullet as a circle

# target class
class Target(pygame.sprite.Sprite):
    def __init__(self,image_path,size = (50,50)):
        super().__init__()
        self.set_image(image_path, size)
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(80, height - self.rect.height)

    def set_image(self, image_path, size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()  

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# time_target class
class Time_target(Target):
    def __init__(self):
        super().__init__('clock.png',(30,30))
    
    # def draw(self,screen):
    #     pygame.draw.circle(screen,(0,0,0),self.rect.center,10)


# bullet_target class
class Bullet_target(Target):
    def __init__(self):
        super().__init__('arrow.png',(50,50))

    # def draw(self,screen):
    #     screen.blit(self.image , (self.rect.x , self.rect.y))
# score_target class
class Score_target(Target):
    def __init__(self):
        super().__init__('score.png',(50,50))
    
    # def draw(self,screen):
    #     pygame.draw.rect(screen,(0,0,0),self.rect)
    
#to create screen 
screen = pygame.display.set_mode((width,height))

#to create title for game
pygame.display.set_caption("CShot_E3")

#to set a background
background = pygame.image.load('aaa.png')
background = pygame.transform.scale(background,(width,height))

# Create player
p1 = Player()
p2 = Player(is_player1=False)

# Set player random position
p1.random_position()
p2.random_position()

#p2.surf.fill((0,0,0))

targets = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(p2)

# Update the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            p1.shoot(event)
            p2.shoot(event)

    # Decrease player time
    p1.time -= 1 / 60  # Decrease time for Player 1 (1 second per 60 frames)
    p2.time -= 1 / 60  # Decrease time for Player 2
    # prevent time from going negative
    p1.time = max(0, p1.time)
    p2.time = max(0, p2.time)
    if p1.time <= 10 or p2.time <= 10 :
        tictac.play()
    # End the game if time runs out
    if p1.time <= 0 and p2.time <= 0:
        print("Game Over!")
        exit()

    # End the game if bullets end
    if p1.num <= 0 and p2.num <= 0:
        print("Game Over!")
        exit()

    # Player actions
    p1.move()
    p2.move()

    # Draw everything
    screen.blit(background, (0, 0))
    for enity in all_sprites:
        if type(enity) == Bullet:
            enity.draw(screen)
    for target in targets:
        target.draw(screen)

    if len(targets) < 7:
        # Define target types and their probabilities
        target_types = [Time_target, Bullet_target, Score_target]
        target_weights = [0.15, 0.15, 0.7]  # Probabilities: 15% Time, 15% Bullet, 70% Score

        # Create a new target based on weighted probabilities
        new_target_class = random.choices(target_types, weights=target_weights, k=1)[0]
        new_target = new_target_class()

        # Check for collisions with existing targets
        collision = True
        while collision:
            collision = False
            for existing_target in targets:
                if new_target.rect.colliderect(existing_target.rect):
                    # If there's a collision, reposition the new target
                    new_target.rect.x = random.randint(0, width - new_target.rect.width)
                    new_target.rect.y = random.randint(80, height - new_target.rect.height)
                    collision = True  # Continue checking for collisions
                    break

        # Add the new target to the game
        targets.add(new_target)

    # Check for collision
    for bullet in bullets:
        for target in targets:
            if bullet.rect.colliderect(target.rect):
                if type(target) == Time_target:
                    if bullet.is_player1:
                        p1.time += 5
                    else:
                        p2.time += 5
                if type(target) == Bullet_target:
                    if bullet.is_player1:
                        p1.num += 3
                    else:
                        p2.num += 3
                if type(target) == Score_target:
                    score_sound.play()
                    if bullet.is_player1:
                        p1.score += 100
                    else:
                        p2.score += 100
                targets.remove(target)
                all_sprites.remove(target)
                bullets.remove(bullet)
                all_sprites.remove(bullet)

    # Display remaining time, bullets, and score
    p1_time_text = font.render(f"{username1} Time: {int(p1.time)}", True, (255, 255, 0))
    p2_time_text = font.render(f"{username2} Time: {int(p2.time)}", True, (0, 255, 255))
    p1_bullet_text = font.render(f"{username1} Bullets: {p1.num}", True, (255, 255, 0))
    p2_bullet_text = font.render(f"{username2} Bullets: {p2.num}", True, (0, 255, 255))
    p1_score_text = font.render(f"{username1} Score: {p1.score}", True, (255, 255, 0))
    p2_score_text = font.render(f"{username2} Score: {p2.score}", True, (0, 255, 255))

    # Display Player 1's stats
    screen.blit(p1_time_text, (10, 10))  # Time at the top-left
    screen.blit(p1_bullet_text, (10, 40))  # Bullets below time
    screen.blit(p1_score_text, (10, 70))  # Score below bullets

    # Display Player 2's stats
    screen.blit(p2_time_text, (700, 10))  # Time at the top-right
    screen.blit(p2_bullet_text, (700, 40))  # Bullets below time
    screen.blit(p2_score_text, (700, 70))  # Score below bullets

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)  # Limit the frame rate to 60 FPS