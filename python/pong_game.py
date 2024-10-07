import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Create paddles and ball
player1 = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Set up the game clock
clock = pygame.time.Clock()

# Initialize scores
score1 = 0
score2 = 0

# Font for displaying scores
font = pygame.font.Font(None, 36)

def move_paddle(keys, player):
    if keys[pygame.K_w] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

def move_paddle2(keys, player):
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

def move_ball(ball, ball_speed_x, ball_speed_y):
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    return ball_speed_x, ball_speed_y

def check_ball_collision(ball, player1, player2, ball_speed_x, ball_speed_y):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    return ball_speed_x, ball_speed_y

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    return BALL_SPEED_X, BALL_SPEED_Y

# Main game loop
ball_speed_x, ball_speed_y = BALL_SPEED_X, BALL_SPEED_Y

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    move_paddle(keys, player1)
    move_paddle2(keys, player2)

    ball_speed_x, ball_speed_y = move_ball(ball, ball_speed_x, ball_speed_y)
    ball_speed_x, ball_speed_y = check_ball_collision(ball, player1, player2, ball_speed_x, ball_speed_y)

    # Check for scoring
    if ball.left <= 0:
        score2 += 1
        ball_speed_x, ball_speed_y = reset_ball()
    elif ball.right >= WIDTH:
        score1 += 1
        ball_speed_x, ball_speed_y = reset_ball()

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw the center line
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Display scores
    score_display1 = font.render(str(score1), True, WHITE)
    score_display2 = font.render(str(score2), True, WHITE)
    screen.blit(score_display1, (WIDTH//4, 20))
    screen.blit(score_display2, (3*WIDTH//4, 20))

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)