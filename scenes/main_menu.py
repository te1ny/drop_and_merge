import pygame
import os
import config
from scenes.base_scene import Scene

class Button:
    def __init__(self, rect, text, action, font, sound=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = font
        self.sound = sound
        self.color = pygame.Color('gray')
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

class MainMenuScene(Scene):
    def __init__(self, manager, screen_size):
        super().__init__(manager)
        self.screen_width, self.screen_height = screen_size
        self.font = pygame.font.SysFont('Arial', 36)
        self.button_click_sound = None

        if os.path.exists(config.BUTTON_CLICK_SOUND_FILE):
            self.button_click_sound = pygame.mixer.Sound(config.BUTTON_CLICK_SOUND_FILE)
            self.button_click_sound.set_volume(config.SOUND_VOLUME)

        self.buttons = []
        button_width = 300
        button_height = 50
        spacing = 20
        start_y = self.screen_height // 3
        center_x = self.screen_width // 2 - button_width // 2
        actions = [self.start_game, self.open_settings, self.open_shop, self.quit_game]
        texts = ["Начать игру", "Настройки", "Магазин", "Выйти"]

        for i in range(4):
            btn_rect = (center_x, start_y + i * (button_height + spacing), button_width, button_height)
            btn = Button(btn_rect, texts[i], actions[i], self.font, sound=self.button_click_sound)
            self.buttons.append(btn)

    def start_game(self):
        from scenes.game_session import GameSessionScene
        self.manager.game_session = GameSessionScene(self.manager, (self.screen_width, self.screen_height))
        self.manager.go_to(self.manager.game_session)

    def open_settings(self):
        from scenes.settings_scene import SettingsScene
        self.manager.go_to(SettingsScene(self.manager, (self.screen_width, self.screen_height)))

    def open_shop(self):
        from scenes.shop_scene import ShopScene
        self.manager.go_to(ShopScene(self.manager, (self.screen_width, self.screen_height)))

    def quit_game(self):
        pygame.quit()
        exit()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for btn in self.buttons:
                    if btn.is_clicked(pos):
                        btn.click()
                        btn.action()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(pygame.Color('white'))
        for btn in self.buttons:
            btn.draw(screen)
