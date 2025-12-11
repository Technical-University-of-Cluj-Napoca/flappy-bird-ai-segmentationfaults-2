import pygame
import os

pygame.init()

win_height = 720
win_width = 551
scroll_speed = 1


score = 0

font = pygame.font.SysFont('Segoe', 26)
small_font = pygame.font.SysFont('Arial', 16)



show_score_popup = False  

SCORE_FILE = "highscore.txt"

ORIGINAL_WIDTH = 288
ORIGINAL_HEIGHT = 512
SCALE = win_width / ORIGINAL_WIDTH  

GROUND_HEIGHT = int(112 * SCALE * 0.6)  

bird_start_position = (100, 300)

BUTTON_WIDTH = int(104 * SCALE * 0.6)
BUTTON_HEIGHT = int(58 * SCALE * 0.5)

STATE_MENU = 0
STATE_GET_READY = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3

def scale_image(image, scale_factor):
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))


bird_scale = SCALE * 0.7  
bird_images = [scale_image(pygame.image.load("sprites/redbird-downflap.png"), bird_scale),
               scale_image(pygame.image.load("sprites/redbird-midflap.png"), bird_scale),
               scale_image(pygame.image.load("sprites/redbird-upflap.png"), bird_scale)]

_ground_raw = pygame.image.load("sprites/base.png")
ground_image = pygame.transform.scale(_ground_raw, (win_width + 100, GROUND_HEIGHT))

PLAYABLE_HEIGHT = win_height - GROUND_HEIGHT  


_top_pipe_raw = pygame.image.load("sprites/pipe-green-down.png")
_bottom_pipe_raw = pygame.image.load("sprites/pipe-green.png")
pipe_width = int(_top_pipe_raw.get_width() * SCALE * 0.7)  
pipe_height = 500  
top_pipe_image = pygame.transform.scale(_top_pipe_raw, (pipe_width, pipe_height))
bottom_pipe_image = pygame.transform.scale(_bottom_pipe_raw, (pipe_width, pipe_height))

game_over_image = scale_image(pygame.image.load("sprites/gameover.png"), SCALE * 0.8)
start_image = scale_image(pygame.image.load("sprites/start.png"), SCALE * 0.8)
message_image = scale_image(pygame.image.load("sprites/message.png"), SCALE * 0.7)

number_scale = SCALE * 1.2
number_images = [scale_image(pygame.image.load(f"sprites/{i}.png"), number_scale) for i in range(10)]

small_number_scale = SCALE * 0.35
small_number_images = [scale_image(pygame.image.load(f"sprites/{i}.png"), small_number_scale) for i in range(10)]

tiny_number_scale = SCALE * 0.3
tiny_number_images = [scale_image(pygame.image.load(f"sprites/{i}.png"), tiny_number_scale) for i in range(10)]


medal_scale = SCALE * 0.22  
bronze_medal = scale_image(pygame.image.load("sprites/bronze_medal.png"), medal_scale)
silver_medal = scale_image(pygame.image.load("sprites/silver_medal.png"), medal_scale)
gold_medal = scale_image(pygame.image.load("sprites/gold_medal.png"), medal_scale)
platinum_medal = scale_image(pygame.image.load("sprites/platinum_medal.png"), medal_scale)

MEDAL_THRESHOLDS = {
    'bronze': 10,
    'silver': 20,
    'gold': 30,
    'platinum': 40
}

def get_medal(score):
    if score >= MEDAL_THRESHOLDS['platinum']:
        return platinum_medal
    elif score >= MEDAL_THRESHOLDS['gold']:
        return gold_medal
    elif score >= MEDAL_THRESHOLDS['silver']:
        return silver_medal
    elif score >= MEDAL_THRESHOLDS['bronze']:
        return bronze_medal
    return None

MEDAL_PLACEHOLDER_RADIUS = int(20 * SCALE * 0.22)


