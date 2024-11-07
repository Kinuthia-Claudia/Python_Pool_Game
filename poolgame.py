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