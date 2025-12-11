import pygame
import random
from bird import Bird
from pipe import Pipe
from ground import Ground
from utils import *
from score import *
from ui import *
from game_modules.game_config import config
from ai.population import Population

class GameController:
    def __init__(self):
        self.bird = None
        self.pipes = None
        self.ground = None
        self.pipe_timer = 0
        self.pause_btn_rect = None
        self.ai_mode = False
        self.population = None
        
    def initialize_game(self):
        config.reset_game()
        if getattr(config, 'start_with_ai', False):
            self.ai_mode = True
            self.population = Population(config.ai_population_size)
            self.pipe_timer = 0
            self.pipes = pygame.sprite.Group()
            y_pos_ground = win_height - ground_image.get_height()
            self.ground = pygame.sprite.Group()
            self.ground.add(Ground(0, y_pos_ground))
            config.start_with_ai = False
        else:
            self.bird = pygame.sprite.GroupSingle()
            self.bird.add(Bird())

            self.pipe_timer = 0
            self.pipes = pygame.sprite.Group()

            y_pos_ground = win_height - ground_image.get_height()
            self.ground = pygame.sprite.Group()
            self.ground.add(Ground(0, y_pos_ground))
        
        pause_btn_x = 15
        pause_btn_y = 15
        self.pause_btn_rect = pygame.Rect(pause_btn_x, pause_btn_y, pause_button_img.get_width(),
                         pause_button_img.get_height())
        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save_high_score(config.best_score)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
                
    def _handle_key_press(self, key):
        if key == pygame.K_SPACE and not config.is_paused:
            if self.bird.sprite.alive and self.bird.sprite.rect.y > 0:
                self.bird.sprite.flap = True
                self.bird.sprite.vel = -7
        elif key == pygame.K_p or key == pygame.K_ESCAPE:
            config.is_paused = not config.is_paused
            
    def _handle_mouse_click(self, mouse_pos):
        if self.pause_btn_rect.collidepoint(mouse_pos):
            config.is_paused = not config.is_paused
        elif not config.is_paused:
            if self.bird and self.bird.sprite and self.bird.sprite.alive and self.bird.sprite.rect.y > 0:
                self.bird.sprite.flap = True
                self.bird.sprite.vel = -7

        return
                
    def update(self):
        if config.is_paused:
            return
        # AI mode update
        if self.ai_mode and self.population is not None:
            # update pipes and ground
            self.pipes.update()
            self.ground.update()

            if self.pipe_timer <= 0:
                self._spawn_pipes()
                self.pipe_timer = random.randint(180, 250)
            self.pipe_timer -= 1

            # update population (draw/update handled there)
            self.population.update_live_players(self.pipes)

            # Update historical best every frame (not just during selection)
            try:
                current_best = max(getattr(b, 'score', 0) for b in self.population.birds)
                if current_best > self.population.historical_best:
                    self.population.historical_best = current_best
                    print(f'[Gen {self.population.generation}] New best score: {self.population.historical_best}')
            except Exception:
                pass

            if self.population.extinct():
                # prepare next generation
                self.pipes.empty()
                self.population.natural_selection()
            return

        # Single-player update
        if self.bird.sprite.alive:
            self.pipes.update()
            self.ground.update()

            for pipe in self.pipes:
                if pipe.pipe_type == 'bottom' and not pipe.passed:
                    if self.bird.sprite.rect.left > pipe.rect.right:
                        pipe.passed = True
                        config.score += 1

        user_input = pygame.key.get_pressed()
        self.bird.update(user_input)

        collision_pipes = pygame.sprite.spritecollide(self.bird.sprites()[0], self.pipes, False)
        collision_ground = pygame.sprite.spritecollide(self.bird.sprites()[0], self.ground, False)

        if collision_pipes or collision_ground:
            self.bird.sprite.alive = False
            config.update_best_score(config.score)
            config.game_state = STATE_GAME_OVER
            return

        if self.pipe_timer <= 0 and self.bird.sprite.alive:
            self._spawn_pipes()
            self.pipe_timer = random.randint(180, 250)
        self.pipe_timer -= 1
        
    def _spawn_pipes(self):
        y_pos_ground = win_height - ground_image.get_height()
        x_pos = win_width + 10
        pipe_gap = random.randint(140, 180)
        
        min_gap_top = 80
        max_gap_top = y_pos_ground - pipe_gap - 80
        gap_top = random.randint(min_gap_top, max_gap_top)
        
        y_top = gap_top - top_pipe_image.get_height()
        y_bottom = gap_top + pipe_gap
        
        self.pipes.add(Pipe(x_pos, y_top, top_pipe_image, 'top'))
        self.pipes.add(Pipe(x_pos, y_bottom, bottom_pipe_image, 'bottom'))
        
    def render(self):
        y_pos_ground = win_height - ground_image.get_height()
        
        config.window.fill((0, 0, 0))
        config.window.blit(skyline_image, (0, 0))
        
        if len(self.ground) <= 2:
            self.ground.add(Ground(win_width, y_pos_ground))
        
        self.pipes.draw(config.window)
        self.ground.draw(config.window)
        if self.ai_mode and self.population is not None:
            for b in self.population.birds:
                if getattr(b, 'alive', False):
                    b.draw(config.window)
            # HUD indicator for AI mode: generation / alive / best fitness
            try:
                alive = sum(1 for b in self.population.birds if getattr(b, 'alive', False))
                total = len(self.population.birds)
                gen = getattr(self.population, 'generation', 0)
                # best score among birds
                best_score = 0
                for b in self.population.birds:
                    if getattr(b, 'score', 0) > best_score:
                        best_score = b.score

                font = pygame.font.SysFont('Arial', 18, bold=True)
                # draw at bottom-left: two lines (Gen, Alive)
                lines = [f'Gen: {gen}', f'Alive: {alive}/{total}']
                start_y = win_height - 40
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255, 255, 255))
                    config.window.blit(text, (10, start_y + i * 20))
            except Exception:
                pass
        else:
            self.bird.draw(config.window)
        
        # In AI mode show historical best score (all-time across generations) at top-center
        if self.ai_mode and self.population is not None:
            # Use historical_best so the displayed score persists and increases as evolution improves
            best_score = getattr(self.population, 'historical_best', 0)
            draw_score(config.window, best_score, win_width // 2, 50, centered=True)
        else:
            draw_score(config.window, config.score, win_width // 2, 50, centered=True)
        
        if config.is_paused:
            config.window.blit(resume_button_img, (self.pause_btn_rect.x, self.pause_btn_rect.y))
            
            pause_font = pygame.font.SysFont('Arial', 40, bold=True)
            pause_text = pause_font.render('PAUSED', True, (255, 255, 255))
            pause_shadow = pause_font.render('PAUSED', True, (0, 0, 0))
            text_x = win_width // 2 - pause_text.get_width() // 2
            text_y = win_height // 2 - pause_text.get_height() // 2
            config.window.blit(pause_shadow, (text_x + 2, text_y + 2))
            config.window.blit(pause_text, (text_x, text_y))
        else:
            config.window.blit(pause_button_img, (self.pause_btn_rect.x, self.pause_btn_rect.y))
        
        pygame.display.update()
        config.clock.tick(60)
        
    def get_game_state(self):
        return self.pipes, self.ground, self.bird, win_height - ground_image.get_height()
