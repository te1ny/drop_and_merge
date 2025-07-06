import pygame
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

class ShopScene(Scene):
    def __init__(self, manager, screen_size):
        super().__init__(manager)
        self.screen_width, self.screen_height = screen_size
        self.font = pygame.font.SysFont("Arial", 28)
        self.buttons = []

        booster_names = ["x2", "x3", "x10"]
        start_y = 150
        spacing_y = 80
        button_width = 100
        button_height = 40

        for i, booster in enumerate(booster_names):
            y = start_y + i * spacing_y

            buy_rect = (50, y, button_width, button_height)
            use_rect = (200, y, button_width, button_height)

            buy_button = Button(buy_rect, "Buy", lambda b=booster: self.buy_booster(b), self.font, sound=None)
            use_button = Button(use_rect, "Use", lambda b=booster: self.use_booster(b), self.font, sound=None)

            self.buttons.append((booster, buy_button, use_button))

        self.back_button = Button((10, 10, 100, 40), "Назад", self.go_back, self.font, sound=None)

    def buy_booster(self, booster):
        price = config.BOOSTER_PRICES[booster]
        if config.PLAYER_COINS >= price:
            config.PLAYER_COINS -= price
            config.PLAYER_BOOSTERS[booster] += 1

    def use_booster(self, booster):
        if config.PLAYER_BOOSTERS[booster] > 0:
            config.PLAYER_BOOSTERS[booster] -= 1
            multiplier = float(booster[1:])
            config.PLAYER_ACTIVE_BOOSTERS.append(multiplier)

    def go_back(self):
        from scenes.main_menu import MainMenuScene
        self.manager.go_to(MainMenuScene(self.manager, (self.screen_width, self.screen_height)))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.back_button.is_clicked(pos):
                    self.back_button.click()
                    self.go_back()
                for booster, buy_btn, use_btn in self.buttons:
                    if buy_btn.is_clicked(pos):
                        buy_btn.click()
                        self.buy_booster(booster)
                    elif use_btn.is_clicked(pos):
                        use_btn.click()
                        self.use_booster(booster)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(pygame.Color('lightblue'))
        coins_text = f"Монетки: {config.PLAYER_COINS}"
        coins_surf = self.font.render(coins_text, True, pygame.Color('black'))
        screen.blit(coins_surf, (self.screen_width - 200, 20))
        y_offset = 150

        for booster, buy_btn, use_btn in self.buttons:
            text = f"Бустер {booster} | Цена: {config.BOOSTER_PRICES[booster]} | В наличии: {config.PLAYER_BOOSTERS[booster]}"
            text_surf = self.font.render(text, True, pygame.Color('black'))
            screen.blit(text_surf, (50, y_offset - 30))
            buy_btn.draw(screen)
            use_btn.draw(screen)
            y_offset += 80

        title_surf = self.font.render("Магазин", True, pygame.Color('black'))
        title_rect = title_surf.get_rect(center=(self.screen_width//2, 50))
        screen.blit(title_surf, title_rect)
        self.back_button.draw(screen)
