import sqlite3
import pygame
import hashlib
import sys

# Create a function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to the database
conn = sqlite3.connect('game.db')

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    score INTEGER DEFAULT 0
)
''')

pygame.init()

# Define colors
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BLACK = (0,0,0)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Login")

# Enable key repeat events)
pygame.key.set_repeat(500, 50)

# Buttons
sign_in_button = pygame.Rect(300, 400, 100, 50)
sign_up_button = pygame.Rect(410, 400, 100, 50)

font = pygame.font.Font(None, 32)
input_box1 = pygame.Rect(300, 200, 200, 50)
input_box2 = pygame.Rect(300, 300, 200, 50)
active1 = False
active2 = False
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color1 = color_inactive
color2 = color_inactive
usrname = ''
password = ''


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

message = ""
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = not active1
            else:
                active1 = False
            if input_box2.collidepoint(event.pos):
                active2 = not active2
            else:
                active2 = False
            color1 = color_active if active1 else color_inactive
            color2 = color_active if active2 else color_inactive
            if sign_in_button.collidepoint(event.pos):
                #print("Sign In button clicked")
                # sign-in logic
                hashed_password = hash_password(password)
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (usrname, hashed_password))
                user = cursor.fetchone()
                if user:
                    message = 'Login successful'
                    print(usrname)
                    pygame.quit()
                    sys.exit()
                else:
                    message = 'Invalid username or password'
            if sign_up_button.collidepoint(event.pos):
                #print("Sign Up button clicked")
                # sign-up logic 
                try:
                    hashed_password = hash_password(password)
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (usrname, hashed_password))
                    conn.commit()
                    message = 'User created successfully Please sign in'
                except sqlite3.IntegrityError:
                    message = 'User already exists'

        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_RETURN:
                    active1 = False
                    active2 = True
                elif event.key == pygame.K_BACKSPACE:
                    usrname = usrname[:-1]
                else:
                    usrname += event.unicode
            if active2:
                if event.key == pygame.K_RETURN:
                    active2 = False
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode
            color1 = color_active if active1 else color_inactive
            color2 = color_active if active2 else color_inactive
    screen.fill('white')

    # Draw message
    draw_text(message, font, BLACK, screen, 300, 100)   
    draw_text('Username:', font, BLACK, screen, 150, 210)
    draw_text('Password:', font, BLACK, screen, 150, 310)
    # Render the current text.
    txt_surface1 = font.render(usrname, True, color1)
    txt_surface2 = font.render(password, True, color2)
    # Resize the box if the text is too long.
    width1 = max(200, txt_surface1.get_width()+10)
    width2 = max(200, txt_surface2.get_width()+10)
    input_box1.w = width1
    input_box2.w = width2
    # Blit the text.
    screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+15))
    screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+15))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color1, input_box1, 2)
    pygame.draw.rect(screen, color2, input_box2, 2)

    # Draw buttons
    pygame.draw.rect(screen, LIGHT_BLUE, sign_in_button)
    pygame.draw.rect(screen, LIGHT_BLUE, sign_up_button)
    draw_text('Sign In', font, BLACK, screen, sign_in_button.x + 10, sign_in_button.y + 10)
    draw_text('Sign Up', font, BLACK, screen, sign_up_button.x + 10, sign_up_button.y + 10)    

    pygame.display.flip()

pygame.quit()

# Close the database connection
conn.close()