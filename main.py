import pygame
from sys import exit

from utils import *
from game_modules.game_config import config
from game_modules.screens import MenuScreen, GetReadyScreen, GameOverScreen
from game_modules.game_controller import GameController


def initialize_game():
    pygame.init()
    
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Flappy Bird")
    
    config.set_window(window)
    
    return window


def main_loop():
    menu_screen = MenuScreen()
    get_ready_screen = None
    game_controller = None
    game_over_screen = None
    
    while True:
        if config.game_state == STATE_MENU:
            menu_screen.handle_events()
            menu_screen.render()
            
        elif config.game_state == STATE_GET_READY:
            if get_ready_screen is None:
                get_ready_screen = GetReadyScreen()
            
            get_ready_screen.handle_events()
            get_ready_screen.render()
            
        elif config.game_state == STATE_PLAYING:
            if game_controller is None:
                game_controller = GameController()
                game_controller.initialize_game()
            
            game_controller.handle_events()
            game_controller.update()
            game_controller.render()
            
            if config.game_state == STATE_GAME_OVER:
                pipes, ground, bird, y_pos_ground = game_controller.get_game_state()
                game_over_screen = GameOverScreen(pipes, ground, bird, y_pos_ground)
                game_controller = None
                get_ready_screen = None
                
        elif config.game_state == STATE_GAME_OVER:
            game_over_screen.handle_events()
            game_over_screen.render()
            
            if config.game_state == STATE_MENU:
                game_over_screen = None
                get_ready_screen = None


def main():
    initialize_game()
    main_loop()


if __name__ == "__main__":
    main()