import pygame, os, random
from scenes.base_scene import Scene
from objects.ball import Ball
from objects.basket import Basket
import config
from config import ACTIVE_BALL_Y, GRAVITY, FRICTION, ADDITIONAL_RADIUS, BG_COLOR, BACKGROUND_IMAGE_FILE, BUTTON_CLICK_SOUND_FILE, MERGE_SOUND_FILE, COLLISION_SOUND_FILE, BEST_SCORE_FILE, BALL_IS_IMAGE
from config import BALL_DICTIONARY
from physics import simulate_physics

def compute_active_multiplier():
    active = sorted(config.PLAYER_ACTIVE_BOOSTERS, reverse=True)
    total = 1.0
    for i, booster in enumerate(active):
        total += (booster - 1) * (0.5 ** i)
    return total

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
        if self.sound:
            if config.SOUND_VOLUME <= 0:
                return

            self.sound.set_volume(config.SOUND_VOLUME)
            self.sound.play()

class GameSessionScene(Scene):
    def __init__(self, manager, screen_size):
        super().__init__(manager)
        self.screen_width, self.screen_height = screen_size
        self.basket = Basket(self.screen_width, self.screen_height)
        self.balls = []
        active_radius = random.choice([15, 30, 45])
        self.active_ball = Ball((self.screen_width/2, ACTIVE_BALL_Y), active_radius, BALL_IS_IMAGE, BALL_DICTIONARY)
        self.last_release_time = 0
        self.release_delay = 1000  # миллисекунд
        self.font = pygame.font.SysFont('Arial', 24)
        self.score = 0
        self.volume = config.SOUND_VOLUME
        self.coins_awarded = False   # флаг, чтобы монеты начислялись только один раз
        
        if os.path.exists(MERGE_SOUND_FILE):
            self.merge_sound = pygame.mixer.Sound(MERGE_SOUND_FILE)
            self.merge_sound.set_volume(self.volume)
        else:
            self.merge_sound = None

        if os.path.exists(COLLISION_SOUND_FILE):
            self.collision_sound = pygame.mixer.Sound(COLLISION_SOUND_FILE)
            self.collision_sound.set_volume(self.volume)
        else:
            self.collision_sound = None

        if os.path.exists(BUTTON_CLICK_SOUND_FILE):
            self.button_click_sound = pygame.mixer.Sound(BUTTON_CLICK_SOUND_FILE)
            self.button_click_sound.set_volume(self.volume)
        else:
            self.button_click_sound = None
        
        btn_w = 100
        btn_h = 40

        self.pause_button = Button((10, 10, btn_w, btn_h), "Пауза", self.pause, self.font, sound=self.button_click_sound)
        self.menu_button = Button((120, 10, btn_w, btn_h), "Меню", self.go_menu, self.font, sound=self.button_click_sound)
        self.paused = False
        self.game_over = False
        self.game_over_time = 0

    def pause(self):
        if self.button_click_sound:
            self.button_click_sound.set_volume(config.SOUND_VOLUME)
            if config.SOUND_VOLUME > 0:
                self.button_click_sound.play()

        self.paused = not self.paused

    def go_menu(self):
        if self.button_click_sound:
            self.button_click_sound.set_volume(config.SOUND_VOLUME)

            if config.SOUND_VOLUME > 0:
                self.button_click_sound.play()

        from scenes.main_menu import MainMenuScene
        self.manager.go_to(MainMenuScene(self.manager, (self.screen_width, self.screen_height)))

    def handle_events(self, events):
        for event in events:
            if self.paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.pause_button.is_clicked(event.pos):
                        self.pause()
                    elif self.menu_button.is_clicked(event.pos):
                        self.go_menu()
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_button.is_clicked(event.pos):
                    self.pause()
                elif self.menu_button.is_clicked(event.pos):
                    self.go_menu()
                else:
                    if not self.game_over and self.active_ball:
                        if self.button_click_sound:
                            self.button_click_sound.set_volume(config.SOUND_VOLUME)
                            if config.SOUND_VOLUME > 0:
                                self.button_click_sound.play()
                        self.balls.append(self.active_ball)
                        self.active_ball = None
                        self.last_release_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEMOTION:
                if not self.paused and self.active_ball:
                    mx, _ = event.pos
                    self.active_ball.position[0] = mx
                    self.active_ball.position[1] = ACTIVE_BALL_Y

    def update(self, dt):
        if self.game_over:
            if not self.coins_awarded:
                multiplier = compute_active_multiplier()
                earned = int(self.score * 0.02 * multiplier)
                config.PLAYER_COINS += earned
                self.coins_awarded = True
            if pygame.time.get_ticks() - self.game_over_time > 3000:
                self.save_best_score()
                from scenes.main_menu import MainMenuScene
                self.manager.go_to(MainMenuScene(self.manager, (self.screen_width, self.screen_height)))
            return

        if self.paused:
            return

        if not self.active_ball and pygame.time.get_ticks() - self.last_release_time >= self.release_delay:
            active_radius = random.choice([15, 30, 45])
            self.active_ball = Ball((pygame.mouse.get_pos()[0], ACTIVE_BALL_Y), active_radius, BALL_IS_IMAGE, BALL_DICTIONARY)

        self.balls, merged_count = simulate_physics(
            self.balls, GRAVITY, FRICTION, self.basket, dt=1, iterations=6,
            additional_radius=ADDITIONAL_RADIUS, merge_sound=self.merge_sound, collision_sound=self.collision_sound)
        self.score += merged_count * 20

        for ball in self.balls:
            if ball.is_off_screen(self.screen_width, self.screen_height):
                self.game_over = True
                self.game_over_time = pygame.time.get_ticks()

        if self.active_ball:
            self.active_ball.position[1] = ACTIVE_BALL_Y
            self.active_ball.update_image()

    def render(self, screen):
        if BACKGROUND_IMAGE_FILE and os.path.exists(BACKGROUND_IMAGE_FILE):
            bg = pygame.image.load(BACKGROUND_IMAGE_FILE)
            bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill(BG_COLOR)

        self.basket.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

        if self.active_ball:
            self.active_ball.draw(screen)

        self.pause_button.draw(screen)
        self.menu_button.draw(screen)

        score_surf = self.font.render(f"Счет: {self.score}", True, pygame.Color('black'))
        screen.blit(score_surf, (self.screen_width - 150, 10))

        try:
            with open(BEST_SCORE_FILE, "r") as f:
                best_score = int(f.read())
        except Exception:
            best_score = 0

        best_surf = self.font.render(f"Лучший: {best_score}", True, pygame.Color('black'))
        screen.blit(best_surf, (self.screen_width - 150, 40))
        
        active_text = "Активные бустеры: "
        if config.PLAYER_ACTIVE_BOOSTERS:
            active_text += ", ".join([f"x{int(b)}" for b in config.PLAYER_ACTIVE_BOOSTERS])
            effective = compute_active_multiplier()
            active_text += f" (Эффект: x{effective:.2f})"
        else:
            active_text += "Нет"

        booster_surf = self.font.render(active_text, True, pygame.Color('black'))
        screen.blit(booster_surf, (20, 60))
        
        if self.game_over:
            over_surf = self.font.render("Игра окончена", True, pygame.Color('red'))
            rect = over_surf.get_rect(center=(self.screen_width/2, self.screen_height/2))
            screen.blit(over_surf, rect)

    def save_best_score(self):
        best = 0
        try:
            with open(BEST_SCORE_FILE, "r") as f:
                best = int(f.read())
        except Exception:
            best = 0

        if self.score > best:
            with open(BEST_SCORE_FILE, "w") as f:
                f.write(str(self.score))
