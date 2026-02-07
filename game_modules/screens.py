import pygame
import math
from bird import Bird
from ground import Ground
from utils import *
from score import *
from ui import *
from game_modules.game_config import config
from utils import *


class MenuScreen:
    def __init__(self):
        self.bird_anim_index = 0
        self.bird_anim_index = 0
        self.bird_y_offset = 0
        self.bird_y_direction = 1
        self.current_user_rating = 0
        self.cached_average_rating = 0.0


        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save_high_score(config.best_score)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if config.show_rate_popup:
                    self._handle_rate_clicks(mouse_pos)
                    
                    self._handle_clicks(mouse_pos)
                else:
                    self._handle_clicks(mouse_pos)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            config.game_state = STATE_GET_READY
            
    def _handle_clicks(self, mouse_pos):
        y_pos_ground = win_height - ground_image.get_height()
        button_y_row1 = y_pos_ground - 80
        button_y_row2 = y_pos_ground - 140
        
        
        center = win_width // 2
        spacing = 40
        left_x = center - BUTTON_WIDTH - spacing // 2
        right_x = center + spacing // 2

        start_rect = pygame.Rect(left_x, button_y_row2, BUTTON_WIDTH, BUTTON_HEIGHT)
        rate_rect = pygame.Rect(left_x, button_y_row1, BUTTON_WIDTH, BUTTON_HEIGHT)
        ai_rect = pygame.Rect(right_x, button_y_row2, BUTTON_WIDTH, BUTTON_HEIGHT)
        score_rect = pygame.Rect(right_x, button_y_row1, BUTTON_WIDTH, BUTTON_HEIGHT)

        if rate_rect.collidepoint(mouse_pos):
            config.show_rate_popup = not config.show_rate_popup
            self.current_user_rating = 0
            if config.show_rate_popup:
                self.cached_average_rating = get_average_rating()
            return

        if config.show_rate_popup:
            return


        if start_rect.collidepoint(mouse_pos):
            config.start_with_ai = False
            config.game_state = STATE_GET_READY
            return
        if score_rect.collidepoint(mouse_pos):
            config.show_score_popup = not config.show_score_popup
            return
        if ai_rect.collidepoint(mouse_pos):
            config.start_with_ai = True
            config.game_state = STATE_PLAYING
            return

    def _handle_rate_clicks(self, mouse_pos):
        popup_width = 300
        popup_height = 260
        popup_x = win_width // 2 - popup_width // 2
        popup_y = win_height // 2 - popup_height // 2
        
        close_btn_rect = pygame.Rect(popup_x + popup_width - 30, popup_y + 10, 20, 20)
        if close_btn_rect.collidepoint(mouse_pos):
             config.show_rate_popup = False
             return

        rate_btn_rect = pygame.Rect(popup_x + popup_width//2 - 40, popup_y + 200, 80, 35)
        if rate_btn_rect.collidepoint(mouse_pos):
             if self.current_user_rating > 0:
                 save_rating(self.current_user_rating)
                 self.cached_average_rating = get_average_rating()
             return

        star_y = popup_y + 100
        star_radius = 20
        star_spacing = 50
        start_x = popup_x + (popup_width - (5 * star_spacing)) // 2 + star_radius

        for i in range(1, 6):
            cx = start_x + (i-1) * star_spacing
            cy = star_y
            dist = math.sqrt((mouse_pos[0] - cx)**2 + (mouse_pos[1] - cy)**2)
            if dist <= star_radius * 1.5:
                self.current_user_rating = i
                break



            
    def render(self):
        y_pos_ground = win_height - ground_image.get_height()
        
        button_y_row1 = y_pos_ground - 80
        button_y_row2 = y_pos_ground - 140
        center = win_width // 2
        spacing = 40
        left_x = center - BUTTON_WIDTH - spacing // 2
        right_x = center + spacing // 2
        start_x = left_x
        rate_x = left_x
        ai_x = right_x
        score_x = right_x
        
        config.window.fill((0, 0, 0))
        config.window.blit(skyline_image, (0, 0))
        config.window.blit(ground_image, (0, y_pos_ground))
        
        title_y = win_height // 5
        config.window.blit(title_image, (win_width // 2 - title_image.get_width() // 2, title_y))
        
        self.bird_anim_index = (self.bird_anim_index + 1) % 30
        bird_img = bird_images[self.bird_anim_index // 10]
        
        self.bird_y_offset += self.bird_y_direction * 0.3
        if abs(self.bird_y_offset) > 8:
            self.bird_y_direction *= -1
        
        bird_title_x = win_width // 2 + title_image.get_width() // 2 + 10
        bird_title_y = title_y + title_image.get_height() // 2 - bird_img.get_height() // 2 + self.bird_y_offset
        config.window.blit(bird_img, (bird_title_x, bird_title_y))
        
        config.window.blit(start_button, (start_x, button_y_row2))
        config.window.blit(rate_button, (rate_x, button_y_row1))
        config.window.blit(ai_button, (ai_x, button_y_row2))
        config.window.blit(score_button, (score_x, button_y_row1))
        
        copyright_text = create_copyright_text()
        config.window.blit(copyright_text, (win_width // 2 - copyright_text.get_width() // 2,
                                           y_pos_ground + ground_image.get_height() // 2 - copyright_text.get_height() // 2))
        
        if config.show_score_popup:
            self._render_score_popup(y_pos_ground)
            
        if config.show_rate_popup:
            self._render_rate_popup()

        
        pygame.display.update()
        config.clock.tick(60)
        
    def _render_score_popup(self, y_pos_ground):
        popup_width = 160
        popup_height = 70
        popup_x = win_width // 2 - popup_width // 2
        popup_y = win_height // 2 - popup_height // 2
        
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((223, 216, 149))
        config.window.blit(popup_surface, (popup_x, popup_y))
        pygame.draw.rect(config.window, (211, 170, 98), (popup_x, popup_y, popup_width, popup_height), 3)
        pygame.draw.rect(config.window, (132, 103, 53), (popup_x + 3, popup_y + 3, popup_width - 6, popup_height - 6), 2)
        
        popup_font = pygame.font.SysFont('Arial', 14, bold=True)
        best_label = popup_font.render('BEST SCORE', True, pygame.Color(223, 113, 38))
        config.window.blit(best_label, (popup_x + popup_width // 2 - best_label.get_width() // 2, popup_y + 12))
        
        draw_score(config.window, config.best_score, popup_x + popup_width // 2, popup_y + 35, centered=True, size='tiny')

    def _draw_star(self, surface, x, y, radius, filled, color=(255, 215, 0), outline_color=(255, 255, 255)):
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = radius if i % 2 == 0 else radius * 0.4
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        
        if filled:
            pygame.draw.polygon(surface, color, points)
        else:
            pygame.draw.polygon(surface, (100, 100, 100), points, 2)
            
        pygame.draw.polygon(surface, outline_color, points, 1)

    def _render_rate_popup(self):
        popup_width = 300
        popup_height = 260
        popup_x = win_width // 2 - popup_width // 2
        popup_y = win_height // 2 - popup_height // 2
        
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((223, 216, 149))
        config.window.blit(popup_surface, (popup_x, popup_y))
        pygame.draw.rect(config.window, (211, 170, 98), (popup_x, popup_y, popup_width, popup_height), 3)
        pygame.draw.rect(config.window, (132, 103, 53), (popup_x + 3, popup_y + 3, popup_width - 6, popup_height - 6), 2)
        
        close_rect = pygame.Rect(popup_x + popup_width - 32, popup_y + 8, 24, 24)
        pygame.draw.rect(config.window, (200, 50, 50), close_rect)
        pygame.draw.rect(config.window, (100, 0, 0), close_rect, 2)
        close_font = pygame.font.SysFont('Arial', 18, bold=True)
        close_text = close_font.render("X", True, (255, 255, 255))
        config.window.blit(close_text, (close_rect.centerx - close_text.get_width()//2, close_rect.centery - close_text.get_height()//2))

        popup_font = pygame.font.SysFont('Arial', 24, bold=True)
        title_label = popup_font.render('RATE US', True, pygame.Color(223, 113, 38))
        config.window.blit(title_label, (popup_x + popup_width // 2 - title_label.get_width() // 2, popup_y + 30))
        
        star_y = popup_y + 110
        star_radius = 20
        star_spacing = 50
        start_x = popup_x + (popup_width - (5 * star_spacing)) // 2 + star_radius

        for i in range(1, 6):
            cx = start_x + (i-1) * star_spacing
            cy = star_y
            filled = i <= self.current_user_rating
            self._draw_star(config.window, cx, cy, star_radius, filled)
            
        avg_font = pygame.font.SysFont('Arial', 16, bold=True)
        avg_text = f"Average: {self.cached_average_rating:.1f} / 5.0"
        avg_label = avg_font.render(avg_text, True, (80, 50, 20))
        config.window.blit(avg_label, (popup_x + popup_width // 2 - avg_label.get_width() // 2, popup_y + 160))

        rate_btn_rect = pygame.Rect(popup_x + popup_width//2 - 40, popup_y + 200, 80, 35)
        btn_color = (223, 113, 38)
        pygame.draw.rect(config.window, btn_color, rate_btn_rect)
        pygame.draw.rect(config.window, (180, 80, 20), rate_btn_rect, 2)
        
        btn_font = pygame.font.SysFont('Arial', 18, bold=True)
        btn_text = btn_font.render("RATE", True, (255, 255, 255))
        config.window.blit(btn_text, (rate_btn_rect.centerx - btn_text.get_width()//2, rate_btn_rect.centery - btn_text.get_height()//2))





class GetReadyScreen:
    def __init__(self):
        self.bird = pygame.sprite.GroupSingle()
        self.bird.add(Bird())
        
        y_pos_ground = win_height - ground_image.get_height()
        self.ground = pygame.sprite.Group()
        self.ground.add(Ground(0, y_pos_ground))
        
        pygame.time.wait(200)
        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save_high_score(config.best_score)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                config.game_state = STATE_PLAYING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                config.game_state = STATE_PLAYING
                
    def render(self):
        y_pos_ground = win_height - ground_image.get_height()
        
        config.window.fill((0, 0, 0))
        config.window.blit(skyline_image, (0, 0))
        
        if len(self.ground) <= 2:
            self.ground.add(Ground(win_width, y_pos_ground))
        
        self.ground.draw(config.window)
        self.ground.update()
        
        self.bird.draw(config.window)
        self.bird.sprite.image_index += 1
        if self.bird.sprite.image_index >= 30:
            self.bird.sprite.image_index = 0
        self.bird.sprite.image = bird_images[self.bird.sprite.image_index // 10]
        
        msg_x = win_width // 2 - message_image.get_width() // 2
        msg_y = win_height // 4
        config.window.blit(message_image, (msg_x, msg_y))
        
        pygame.display.update()
        config.clock.tick(60)


class GameOverScreen:    
    def __init__(self, pipes, ground, bird, y_pos_ground):
        self.pipes = pipes
        self.ground = ground
        self.bird = bird
        self.y_pos_ground = y_pos_ground
        
        pygame.time.wait(300)
        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save_high_score(config.best_score)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    config.game_state = STATE_GET_READY
                elif event.key == pygame.K_m:
                    config.game_state = STATE_MENU
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._handle_clicks(mouse_pos)
                
    def _handle_clicks(self, mouse_pos):
        panel_width = int(226 * SCALE * 0.5)
        panel_height = int(114 * SCALE * 0.5)
        game_over_y = win_height // 4
        panel_y = game_over_y + game_over_image.get_height() + 25
        
        btn_y = panel_y + panel_height + 25
        btn_spacing = 30
        
        restart_btn_x = win_width // 2 - restart_button_img.get_width() - btn_spacing // 2
        restart_btn_rect = pygame.Rect(restart_btn_x, btn_y,
                                       restart_button_img.get_width(),
                                       restart_button_img.get_height())
        
        menu_btn_x = win_width // 2 + btn_spacing // 2
        menu_btn_rect = pygame.Rect(menu_btn_x, btn_y,
                                    menu_button_img.get_width(),
                                    menu_button_img.get_height())
        
        if restart_btn_rect.collidepoint(mouse_pos):
            config.game_state = STATE_GET_READY
        elif menu_btn_rect.collidepoint(mouse_pos):
            config.game_state = STATE_MENU
            
    def render(self):
        panel_font = pygame.font.SysFont('Arial', 14, bold=True)
        
        game_over_y = win_height // 4
        panel_width = int(226 * SCALE * 0.5)
        panel_height = int(114 * SCALE * 0.5)
        panel_y = game_over_y + game_over_image.get_height() + 25
        
        btn_y = panel_y + panel_height + 25
        btn_spacing = 30
        
        restart_btn_x = win_width // 2 - restart_button_img.get_width() - btn_spacing // 2
        menu_btn_x = win_width // 2 + btn_spacing // 2
        
        config.window.fill((0, 0, 0))
        config.window.blit(skyline_image, (0, 0))
        
        self.pipes.draw(config.window)
        self.ground.draw(config.window)
        self.bird.draw(config.window)
        
        config.window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2, game_over_y))
        
        panel_x = win_width // 2 - panel_width // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.fill((223, 216, 149))
        config.window.blit(panel_surface, (panel_x, panel_y))
        
        pygame.draw.rect(config.window, (211, 170, 98), (panel_x, panel_y, panel_width, panel_height), 4)
        pygame.draw.rect(config.window, (132, 103, 53), (panel_x + 4, panel_y + 4, panel_width - 8, panel_height - 8), 2)
        
        medal_section_x = panel_x + panel_width * 0.25
        medal_label = panel_font.render('MEDAL', True, (223, 113, 38))
        config.window.blit(medal_label, (medal_section_x - medal_label.get_width() // 2, panel_y + 12))
        
        medal = get_medal(config.score)
        medal_center_x = int(medal_section_x)
        medal_center_y = panel_y + panel_height // 2 + 10
        
        if medal:
            medal_x = medal_center_x - medal.get_width() // 2
            medal_y = medal_center_y - medal.get_height() // 2
            config.window.blit(medal, (medal_x, medal_y))
        else:
            pygame.draw.circle(config.window, (200, 190, 130), (medal_center_x, medal_center_y), 18)
            pygame.draw.circle(config.window, (180, 170, 110), (medal_center_x, medal_center_y), 18, 2)
        
        score_section_x = panel_x + panel_width * 0.72
        
        score_label = panel_font.render('SCORE', True, (223, 113, 38))
        config.window.blit(score_label, (score_section_x - score_label.get_width() // 2, panel_y + 12))
        draw_score(config.window, config.score, int(score_section_x), panel_y + 30, centered=True, size='small')
        
        best_label = panel_font.render('BEST', True, (223, 113, 38))
        config.window.blit(best_label, (score_section_x - best_label.get_width() // 2, panel_y + 58))
        draw_score(config.window, config.best_score, int(score_section_x), panel_y + 76, centered=True, size='small')
        
        config.window.blit(restart_button_img, (restart_btn_x, btn_y))
        config.window.blit(menu_button_img, (menu_btn_x, btn_y))
        
        pygame.display.update()
        config.clock.tick(60)
