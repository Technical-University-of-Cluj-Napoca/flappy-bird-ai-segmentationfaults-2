import pygame
from score import load_high_score, save_high_score
from utils import *

class GameConfig:
    def __init__(self):
        self.window = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Segoe', 26)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        self.game_state = STATE_MENU
        self.score = 0
        self.best_score = load_high_score()
        self.show_score_popup = False
        self.is_paused = False
        # AI settings
        self.ai_population_size = 50
        self.start_with_ai = False
        
    def reset_game(self):
        self.score = 0
        self.is_paused = False
        
    def update_best_score(self, new_score):
        if new_score > self.best_score:
            self.best_score = new_score
            save_high_score(self.best_score)
            
    def set_window(self, window):
        self.window = window
        
    def get_font(self):
        return self.font
    
    def get_small_font(self):
        return self.small_font
    
    def get_clock(self):
        return self.clock

config = GameConfig()