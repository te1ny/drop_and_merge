import pygame
from scenes.base_scene import Scene
import os
import config

class Button:
    def __init__(self, rect, text, action, font, sound=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = font
        self.sound = sound
        self.color = pygame.Color('lightgray')
        self.text_color = pygame.Color('black')
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    def click(self):
        if config.SOUND_VOLUME <= 0:
            return
        if self.sound:
            self.sound.set_volume(config.SOUND_VOLUME)
            self.sound.play()

class SettingsScene(Scene):
    def __init__(self, manager, screen_size):
        super().__init__(manager)
        self.screen_width, self.screen_height = screen_size
        self.font = pygame.font.SysFont('Arial', 28)
        self.volume = config.SOUND_VOLUME  
        btn_size = 50
        spacing = 20
        self.btn_decrease_rect = pygame.Rect(
            self.screen_width//2 - btn_size - spacing, self.screen_height//2, btn_size, btn_size)
        self.btn_increase_rect = pygame.Rect(
            self.screen_width//2 + spacing, self.screen_height//2, btn_size, btn_size)
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        self.button_click_sound = None
        if os.path.exists(config.BUTTON_CLICK_SOUND_FILE):
            self.button_click_sound = pygame.mixer.Sound(config.BUTTON_CLICK_SOUND_FILE)
            self.button_click_sound.set_volume(self.volume)
        self.back_button = Button(self.back_button_rect, "Назад", None, self.font, sound=self.button_click_sound)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.is_clicked(event.pos):
                    self.back_button.click()
                    from scenes.main_menu import MainMenuScene
                    self.manager.go_to(MainMenuScene(self.manager, (self.screen_width, self.screen_height)))
                elif self.btn_decrease_rect.collidepoint(event.pos):
                    if self.button_click_sound:
                        self.button_click_sound.set_volume(config.SOUND_VOLUME)
                        if config.SOUND_VOLUME > 0:
                            self.button_click_sound.play()
                    self.volume = max(0.0, self.volume - 0.1)
                    config.SOUND_VOLUME = self.volume
                    pygame.mixer.music.set_volume(self.volume)
                elif self.btn_increase_rect.collidepoint(event.pos):
                    if self.button_click_sound:
                        self.button_click_sound.set_volume(config.SOUND_VOLUME)
                        if config.SOUND_VOLUME > 0:
                            self.button_click_sound.play()
                    self.volume = min(1.0, self.volume + 0.1)
                    config.SOUND_VOLUME = self.volume
                    pygame.mixer.music.set_volume(self.volume)
    def update(self, dt):
        pass
    def render(self, screen):
        screen.fill(config.BG_COLOR)
        self.back_button.draw(screen)
        vol_surf = self.font.render(f"Громкость: {int(self.volume*100)}%", True, pygame.Color('black'))
        vol_rect = vol_surf.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        screen.blit(vol_surf, vol_rect)
        pygame.draw.rect(screen, pygame.Color('lightgray'), self.btn_decrease_rect)
        minus_surf = self.font.render("-", True, pygame.Color('black'))
        minus_rect = minus_surf.get_rect(center=self.btn_decrease_rect.center)
        screen.blit(minus_surf, minus_rect)
        pygame.draw.rect(screen, pygame.Color('lightgray'), self.btn_increase_rect)
        plus_surf = self.font.render("+", True, pygame.Color('black'))
        plus_rect = plus_surf.get_rect(center=self.btn_increase_rect.center)
        screen.blit(plus_surf, plus_rect)
