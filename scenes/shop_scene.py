import pygame
from scenes.base_scene import Scene
from config import BG_COLOR, BUTTON_CLICK_SOUND_FILE
import os

class ShopScene(Scene):
    def __init__(self, manager, screen_size):
        super().__init__(manager)
        self.screen_width, self.screen_height = screen_size
        self.font = pygame.font.SysFont('Arial', 28)
        btn_w = 150
        btn_h = 40
        self.back_button_rect = pygame.Rect(10, 10, btn_w, btn_h)
        self.button_click_sound = None
        if os.path.exists(BUTTON_CLICK_SOUND_FILE):
            self.button_click_sound = pygame.mixer.Sound(BUTTON_CLICK_SOUND_FILE)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button_rect.collidepoint(event.pos):
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    from scenes.main_menu import MainMenuScene
                    self.manager.go_to(MainMenuScene(self.manager, (self.screen_width, self.screen_height)))
    def update(self, dt):
        pass
    def render(self, screen):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, pygame.Color('lightgray'), self.back_button_rect)
        back_surf = self.font.render("Назад", True, pygame.Color('black'))
        screen.blit(back_surf, self.back_button_rect.move(10,5))
        title = self.font.render("Магазин бустеров (скоро)", True, pygame.Color('black'))
        rect = title.get_rect(center=(self.screen_width/2, self.screen_height/2))
        screen.blit(title, rect)
