import pygame
from game.components.spaceship import Spaceship
from game.utils.constants import  BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from game.components.enemies.enemy_manager import EnemyManager
from game.components.bullets.bullet_manager import BulletManager
from game.components.menu import Menu

class Game:

    def __init__(self):
        self.scores = []
        self.best_score = 0
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.playing = False
        self.game_speed = 10
        
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.menu = Menu('Press any key to start...', self.screen)
        self.CURRENT_LEVEL= 1
        self.ENEMIES_PER_LEVEL = 10
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
    
    def run(self):
        pygame.time.delay(120)
        self.enemy_manager.reset()
        self.CURRENT_LEVEL= 1
        self.ENEMIES_PER_LEVEL = 10
        self.score = 0
        
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
    
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self, self.ENEMIES_PER_LEVEL)
        self.bullet_manager.update(self)
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))
        
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.draw_lvl()
        pygame.display.update()
        pygame.display.flip()
        
    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg = self.y_pos_bg + self.game_speed
        
    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH //2
        if self.death_count == 0:
            self.menu.draw(self.screen)
        else:
            self.messages = [
            ("Game over. Press any key to restart...", 0),
            (f'Your score: {self.score}', 50),
            (f'Highest score: {self.best_score}', 100),
            (f'Total deaths: {self.death_count}', 150),
            (f'Level reached: {self.CURRENT_LEVEL}', 200)
            ]
            for message, margin in self.messages:
                self.menu.update_message(message, margin)
                self.menu.draw(self.screen)

        icon = pygame.transform.scale(ICON, (80,120))
        self.screen.blit(icon, (half_screen_width - 50, half_screen_height -150))
        self.menu.update(self)
        
    def update_score(self):
        self.score +=1
        self.scores.append(self.score)
        self.best_score = max(self.scores)
        if self.score == self.ENEMIES_PER_LEVEL:
            self.CURRENT_LEVEL += 1
            self.ENEMIES_PER_LEVEL += 7
            
        
    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (255,255,255)) 
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 100, 50) 
        self.screen.blit(text, text_rect)   
        
    def draw_lvl(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Current level: {self.CURRENT_LEVEL}', True, (255,255,255)) 
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 150, SCREEN_HEIGHT -20) 
        self.screen.blit(text, text_rect) 