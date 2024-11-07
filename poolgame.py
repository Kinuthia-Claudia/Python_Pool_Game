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