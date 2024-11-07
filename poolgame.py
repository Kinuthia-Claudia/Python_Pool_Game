import pymunk
import pygame
import pymunk.pygame_util
import math
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BOTTOM_PANEL = 50

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Group 9 Mini Project - Pool Game")
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Variables
clock = pygame.time.Clock()
FPS = 120
lives = 3
dia = 36
pocket_dia = 66
force = 0
max_force = 10000
force_direction = 1
cue_angle = 0
game_running = True
cue_ball_potted = False
taking_shot = True
powering_up = False
potted_balls = []
stop_time = 120
shot_start_time = None
taking_shot = True
eight_ball_potted = False
BG = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont("Nunito", 40)
large_font = pygame.font.SysFont("Nunito", 60)
ball_font = pygame.font.SysFont("Nunito", 30)

# Outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Pool ball colors, positions and numbers
ball_data = [
    ((255, 255, 0), "1"),
    ((0, 0, 255), "2"),
    ((255, 0, 0), "3"),
    ((128, 0, 128), "4"),
    ((255, 165, 0), "5"),
    ((128, 0, 0), "6"),
    ((0, 100, 0), "7"),
    ((0, 0, 0), "8"),
    ((0, 128, 0), "9"),
    ((0, 0, 130), "10"),
    ((128, 128, 128), "11"),
    ((255, 20, 147), "12"),
    ((255, 215, 0), "13"),
    ((0, 206, 209), "14"),
    ((255, 99, 71), "15")
]

balls = []
positions = [
    (300, 300),  (264, 320), (264, 284), (228, 338), (228, 302), (228, 266),
    (192, 356), (192, 320), (192, 284), (192, 248), (156, 374), (156, 338),
    (156, 302), (156, 266), (156, 230)
]
# Creating balls
def create_ball(radius, pos, color, number):
    body = pymunk.Body()
    body.damping = 0.95
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.1
    shape.color = color
    shape.number = number
    shape.friction = 10
    space.add(body, shape)
    return shape


for i, (color, number) in enumerate(ball_data):
    pos = positions[i]
    new_ball = create_ball(dia / 2, pos, color, number)
    balls.append(new_ball)

# Cue ball
cue_ball = create_ball(dia / 2, (888, SCREEN_HEIGHT / 2), WHITE, "")
balls.append(cue_ball)

# Create pockets
pockets = [
    (50, 50), (SCREEN_WIDTH // 2, 50), (SCREEN_WIDTH - 50, 50),
    (50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50),
    (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
]

# Create cushions
cushions = [
    [(50, 50), (950, 50), (950, 60), (50, 60)],  # Top
    [(50, 540), (950, 540), (950, 550), (50, 550)],  # Bottom
    [(50, 50), (60, 50), (60, 540), (50, 540)],  # Left
    [(940, 50), (950, 50), (950, 540), (940, 540)]  # Right
]
def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.5
    space.add(body, shape)

for c in cushions:
    create_cushion(c)

# Game loop
run = True
while run:
    clock.tick(FPS)
    space.step(1 / FPS)

    # Pool table
    screen.fill(BG)
    border_width = 28
    table_x = 50
    table_y = 50
    table_width = SCREEN_WIDTH - 100
    table_height = SCREEN_HEIGHT - 100
    pygame.draw.rect(screen, BROWN, (table_x - border_width, table_y - border_width,
                                     table_width + 2 * border_width,
                                     table_height + 2 * border_width))

    pygame.draw.rect(screen, GREEN, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
    for pocket in pockets:
        pygame.draw.circle(screen, BLACK, pocket, pocket_dia // 2)


    # Check for potted balls
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist * 2) + (ball_y_dist * 2))
            if ball_dist <= pocket_dia / 2 + ball.radius / 2:
                if i == len(balls) - 1:
                    lives -= 1
                    cue_ball_potted = True
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)
                else:
                    space.remove(ball.body)  # Remove the ball's body from the physics space
                    balls.remove(ball)
                    potted_balls.append(ball)
                    if ball.number == '8':  # Check if the 8 ball has been potted
                        eight_ball_potted = True

    # Draw balls
    for i, ball in enumerate(balls):
        color = ball.color if i < len(balls) - 1 else WHITE
        pygame.draw.circle(screen, color, (int(ball.body.position[0]), int(ball.body.position[1])),
                           int(ball.radius))
        number_surface = ball_font.render(ball.number, True, BLACK if color != BLACK else WHITE)
        number_rect = number_surface.get_rect(center=(int(ball.body.position[0]), int(ball.body.position[1])))
        screen.blit(number_surface, number_rect)

    # Check ball movement and handle timing
    all_stopped = True
    for ball in balls:
        if abs(ball.body.velocity[0]) > 0.1 or abs(ball.body.velocity[1]) > 0.1:
            all_stopped = False
            break

    if shot_start_time is not None:
        elapsed_time = time.time() - shot_start_time
        if elapsed_time < stop_time:
            deceleration_factor = 1 - (elapsed_time / stop_time)
            for ball in balls:
                ball.body.velocity = (
                    ball.body.velocity[0] * deceleration_factor,
                    ball.body.velocity[1] * deceleration_factor
                )
        else:
            for ball in balls:
                ball.body.velocity = (0, 0)
            shot_start_time = None

    if all_stopped:
        taking_shot = True
        shot_start_time = None

    # Handle cue ball and shooting
    if taking_shot and game_running:
        if cue_ball_potted:
            cue_ball_start_position = (888, SCREEN_HEIGHT / 2)
            balls[-1].body.position = cue_ball_start_position
            balls[-1].body.velocity = (0, 0)  # Reset velocity when repositioning
            cue_ball_potted = False

        mouse_pos = pygame.mouse.get_pos()
        cue_position = balls[-1].body.position
        # Calculate angle from cue ball to mouse
        x_dist = mouse_pos[0] - cue_position[0]
        y_dist = mouse_pos[1] - cue_position[1]
        cue_angle = math.atan2(y_dist, x_dist)

        # Draw cue stick
        cue_length = 100
        cue_end_x = cue_position[0] - cue_length * math.cos(cue_angle)  # Note the minus sign
        cue_end_y = cue_position[1] - cue_length * math.sin(cue_angle)  # Note the minus sign
        pygame.draw.line(screen, BROWN, cue_position, (cue_end_x, cue_end_y), 5)

        if powering_up:
            force += 100 * force_direction
            if force >= max_force or force <= 0:
                force_direction *= -1
            for b in range(math.ceil(force / 2000)):
                pygame.draw.rect(screen, RED, (cue_position[0] - 30 + (b * 15), cue_position[1] + 30, 10, 20))