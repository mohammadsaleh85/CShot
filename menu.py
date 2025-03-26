import pygame
import subprocess

pygame.init()

width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')

# Load button images
start_img = pygame.image.load("image/start_btn.png").convert_alpha()
score_img = pygame.image.load("image/scoreboard.png").convert_alpha()

# Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Create button instances
start_button = Button(100, 200, start_img, 0.8)
scoreboard = Button(450, 120, score_img, 0.4)

# Game loop
run = True
username1 = None  # Store the username
username2 = None
while run:
    screen.fill((202, 228, 241))

    if start_button.draw(screen):
        # Run login.py and capture the username
        result1 = subprocess.run(["python", "login.py"], capture_output=True, text=True)
        username1 = result1.stdout.strip().split("\n")[-1]  # Get the last line of the output
        result2 = subprocess.run(["python", "login.py"], capture_output=True, text=True)
        username2 = result2.stdout.strip().split("\n")[-1]  # Get the last line of the output

        # Run main.py and pass the usernames as arguments
        subprocess.run(["python", "main.py", username1, username2])

    if scoreboard.draw(screen):
        # Run leaderboard.py
        subprocess.run(["python", "leaderboard.py"])
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()