import pygame
import sqlite3

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Leaderboard")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)  # Font for leaderboard text

# Connect to the database
conn = sqlite3.connect('game.db')
cursor = conn.cursor()

# Query the top 10 scores
cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
top_scores = cursor.fetchall()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the leaderboard title
    title_text = font.render("Leaderboard", True, BLACK)
    screen.blit(title_text, (200, 20))

    # Draw the table headers
    header_username = font.render("Username", True, BLACK)
    header_score = font.render("Score", True, BLACK)
    screen.blit(header_username, (100, 80))
    screen.blit(header_score, (400, 80))

    # Draw the top 10 scores
    y_offset = 120  # Starting y-position for the rows
    for username, score in top_scores:
        username_text = font.render(username, True, BLACK)
        score_text = font.render(str(score), True, BLACK)
        screen.blit(username_text, (100, y_offset))
        screen.blit(score_text, (400, y_offset))
        y_offset += 40  # Move to the next row

    # Update the display
    pygame.display.flip()

# Close the database connection
conn.close()
pygame.quit()

