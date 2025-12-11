import pygame
from sys import exit
import random
from bird import Bird
from pipe import Pipe
from ground import Ground
from utils import *
from score import *
from ui import *

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")

score = 0
best_score = load_high_score()  
font = pygame.font.SysFont('Segoe', 26)
small_font = pygame.font.SysFont('Arial', 16)


game_state = STATE_MENU
show_score_popup = False  


def get_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            save_high_score(best_score)  
            pygame.quit()
            exit()
    return events


def check_button_click(pos, button_rect):
    return button_rect.collidepoint(pos)

#SCREENS
def menu_screen():
    global game_state, show_score_popup
    
    y_pos_ground = win_height - ground_image.get_height()
    
    button_y_row1 = y_pos_ground - 80  
    button_y_row2 = y_pos_ground - 140  
    
    start_x = win_width // 2 - BUTTON_WIDTH - 20
    score_x = win_width // 2 + 20
    rate_x = win_width // 2 - BUTTON_WIDTH // 2
    
    start_rect = pygame.Rect(start_x, button_y_row1, BUTTON_WIDTH, BUTTON_HEIGHT)
    score_rect = pygame.Rect(score_x, button_y_row1, BUTTON_WIDTH, BUTTON_HEIGHT)
    rate_rect = pygame.Rect(rate_x, button_y_row2, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    bird_anim_index = 0
    bird_y_offset = 0
    bird_y_direction = 1
    
    show_score_popup = False
    
    while game_state == STATE_MENU:
        events = get_events()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if check_button_click(mouse_pos, start_rect):
                    game_state = STATE_GET_READY
                    return
                elif check_button_click(mouse_pos, score_rect):
                    show_score_popup = not show_score_popup
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = STATE_GET_READY
            return
        
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        
        window.blit(ground_image, (0, y_pos_ground))
        
        title_y = win_height // 5
        window.blit(title_image, (win_width // 2 - title_image.get_width() // 2, title_y))
        
        bird_anim_index = (bird_anim_index + 1) % 30
        bird_img = bird_images[bird_anim_index // 10]
        
        bird_y_offset += bird_y_direction * 0.3
        if abs(bird_y_offset) > 8:
            bird_y_direction *= -1
        
        bird_title_x = win_width // 2 + title_image.get_width() // 2 + 10
        bird_title_y = title_y + title_image.get_height() // 2 - bird_img.get_height() // 2 + bird_y_offset
        window.blit(bird_img, (bird_title_x, bird_title_y))
        
        window.blit(start_button, (start_x, button_y_row1))
        window.blit(score_button, (score_x, button_y_row1))
        window.blit(rate_button, (rate_x, button_y_row2))
        
        copyright_text = create_copyright_text()
        window.blit(copyright_text, (win_width // 2 - copyright_text.get_width() // 2, 
                                     y_pos_ground + ground_image.get_height() // 2 - copyright_text.get_height() // 2))
        
        if show_score_popup:
            popup_width = 160
            popup_height = 70
            popup_x = win_width // 2 - popup_width // 2
            popup_y = win_height // 2 - popup_height // 2
            
            popup_surface = pygame.Surface((popup_width, popup_height))
            popup_surface.fill((223, 216, 149))
            window.blit(popup_surface, (popup_x, popup_y))
            pygame.draw.rect(window, (211, 170, 98), (popup_x, popup_y, popup_width, popup_height), 3)
            pygame.draw.rect(window, (132, 103, 53), (popup_x + 3, popup_y + 3, popup_width - 6, popup_height - 6), 2)
            
            popup_font = pygame.font.SysFont('Arial', 14, bold=True)
            best_label = popup_font.render('BEST SCORE', True, pygame.Color(223, 113, 38))
            window.blit(best_label, (popup_x + popup_width // 2 - best_label.get_width() // 2, popup_y + 12))
            
            draw_score(window, best_score, popup_x + popup_width // 2, popup_y + 35, centered=True, size='tiny')
        
        pygame.display.update()
        clock.tick(60)


def get_ready_screen():
    global game_state
    
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())
    
    y_pos_ground = win_height - ground_image.get_height()
    ground = pygame.sprite.Group()
    ground.add(Ground(0, y_pos_ground))
    
    pygame.time.wait(200)
    
    while game_state == STATE_GET_READY:
        events = get_events()
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = STATE_PLAYING
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = STATE_PLAYING
                return
        
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))
        
        ground.draw(window)
        ground.update()
        
        bird.draw(window)
        bird.sprite.image_index += 1
        if bird.sprite.image_index >= 30:
            bird.sprite.image_index = 0
        bird.sprite.image = bird_images[bird.sprite.image_index // 10]
        
        msg_x = win_width // 2 - message_image.get_width() // 2
        msg_y = win_height // 4
        window.blit(message_image, (msg_x, msg_y))
        
        pygame.display.update()
        clock.tick(60)


def game_screen():
    global game_state, score, best_score
    
    score = 0
    
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())
    
    pipe_timer = 0
    pipes = pygame.sprite.Group()
    
    y_pos_ground = win_height - ground_image.get_height()
    ground = pygame.sprite.Group()
    ground.add(Ground(0, y_pos_ground))
    
    while game_state == STATE_PLAYING:
        events = get_events()
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bird.sprite.alive and bird.sprite.rect.y > 0:
                    bird.sprite.flap = True
                    bird.sprite.vel = -7
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bird.sprite.alive and bird.sprite.rect.y > 0:
                    bird.sprite.flap = True
                    bird.sprite.vel = -7
        
        window.fill((0, 0, 0))
        user_input = pygame.key.get_pressed()
        
        window.blit(skyline_image, (0, 0))
        
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))
        
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)
        
        draw_score(window, score, win_width // 2, 50, centered=True)
        
        if bird.sprite.alive:
            pipes.update()
            ground.update()
            
            for pipe in pipes:
                if pipe.pipe_type == 'bottom' and not pipe.passed:
                    if bird.sprite.rect.left > pipe.rect.right:
                        pipe.passed = True
                        score += 1
        
        bird.update(user_input)
        
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if score > best_score:
                best_score = score
                save_high_score(best_score)
            game_state = STATE_GAME_OVER
            return pipes, ground, bird, y_pos_ground
        
        if pipe_timer <= 0 and bird.sprite.alive:
            x_pos = win_width + 10
            pipe_gap = random.randint(140, 180)
            
            min_gap_top = 80
            max_gap_top = y_pos_ground - pipe_gap - 80
            gap_top = random.randint(min_gap_top, max_gap_top)
            
            y_top = gap_top - top_pipe_image.get_height()
            y_bottom = gap_top + pipe_gap
            
            pipes.add(Pipe(x_pos, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_pos, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1
        
        clock.tick(60)
        pygame.display.update()
    
    return None, None, None, None


def game_over_screen(pipes, ground, bird, y_pos_ground):
    global game_state, score
    
    pygame.time.wait(300)
    
    panel_font = pygame.font.SysFont('Arial', 14, bold=True)
    
    while game_state == STATE_GAME_OVER:
        events = get_events()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = STATE_GET_READY
                    return
                elif event.key == pygame.K_m:
                    game_state = STATE_MENU
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = STATE_GET_READY
                return
        
        window.fill((0, 0, 0))
        
        window.blit(skyline_image, (0, 0))
        
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)
        
        game_over_y = win_height // 4
        window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2, game_over_y))
        
        panel_width = int(226 * SCALE * 0.5)
        panel_height = int(114 * SCALE * 0.5)
        panel_x = win_width // 2 - panel_width // 2
        panel_y = game_over_y + game_over_image.get_height() + 25
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.fill((223, 216, 149))  # Tan/beige color
        window.blit(panel_surface, (panel_x, panel_y))
        
        pygame.draw.rect(window, (211, 170, 98), (panel_x, panel_y, panel_width, panel_height), 4)
        pygame.draw.rect(window, (132, 103, 53), (panel_x + 4, panel_y + 4, panel_width - 8, panel_height - 8), 2)
        
        medal_section_x = panel_x + panel_width * 0.25
        medal_label = panel_font.render('MEDAL', True, (223, 113, 38))
        window.blit(medal_label, (medal_section_x - medal_label.get_width() // 2, panel_y + 12))
        
        medal = get_medal(score)
        medal_center_x = int(medal_section_x)
        medal_center_y = panel_y + panel_height // 2 + 10
        
        if medal:
            medal_x = medal_center_x - medal.get_width() // 2
            medal_y = medal_center_y - medal.get_height() // 2
            window.blit(medal, (medal_x, medal_y))
        else:
            pygame.draw.circle(window, (200, 190, 130), (medal_center_x, medal_center_y), 18)
            pygame.draw.circle(window, (180, 170, 110), (medal_center_x, medal_center_y), 18, 2)
        
        score_section_x = panel_x + panel_width * 0.72
        
        score_label = panel_font.render('SCORE', True, (223, 113, 38))
        window.blit(score_label, (score_section_x - score_label.get_width() // 2, panel_y + 12))
        draw_score(window, score, int(score_section_x), panel_y + 30, centered=True, size='small')
        
        best_label = panel_font.render('BEST', True, (223, 113, 38))
        window.blit(best_label, (score_section_x - best_label.get_width() // 2, panel_y + 58))
        draw_score(window, best_score, int(score_section_x), panel_y + 76, centered=True, size='small')
        
        restart_text = small_font.render('Click or Press R to Restart | M for Menu', True, pygame.Color(255, 255, 255))
        window.blit(restart_text, (win_width // 2 - restart_text.get_width() // 2, panel_y + panel_height + 20))
        
        pygame.display.update()
        clock.tick(60)


def main():
    global game_state
    
    while True:
        if game_state == STATE_MENU:
            menu_screen()
        elif game_state == STATE_GET_READY:
            get_ready_screen()
        elif game_state == STATE_PLAYING:
            result = game_screen()
            if result[0] is not None:
                pipes, ground, bird, y_pos_ground = result
                game_over_screen(pipes, ground, bird, y_pos_ground)


main()
