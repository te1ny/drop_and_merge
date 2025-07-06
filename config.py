import pygame
import colorsys

MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 800
MAX_WINDOW_WIDTH = 1080
MAX_WINDOW_HEIGHT = 1920

DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 800

FPS = 60
GRAVITY = 0.5
FRICTION = 0.99
ADDITIONAL_RADIUS = 15
ACTIVE_BALL_Y = 100

BASKET_HORIZONTAL_MARGIN = 0.05  # 5% от ширины экрана
BASKET_BOTTOM_MARGIN = 0.05      # 5% от высоты экрана
BASKET_HEIGHT_RATIO = 0.4        # корзинка занимает 40% от высоты экрана

BALL_IS_IMAGE = False

total = 25
BALL_DICTIONARY = {}
for i in range(total):
    radius = 15 * (i + 1)
    factor = (i / (total - 1)) ** 0.75
    hue_deg = factor * 270  # от красного (0°) до фиолетового (270°)
    hue = hue_deg / 360.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    color = pygame.Color(int(r*255), int(g*255), int(b*255))
    BALL_DICTIONARY[radius] = (color, f"ball_{radius}.png")

BEST_SCORE_FILE = "best_score.txt"

MERGE_SOUND_FILE = "sounds\\merge_sound.wav"
COLLISION_SOUND_FILE = ""
BUTTON_CLICK_SOUND_FILE = "sounds\\button_click.wav"

BACKGROUND_IMAGE_FILE = None
BG_COLOR = pygame.Color('white')

SOUND_VOLUME = 1.0

PLAYER_COINS = 0
PLAYER_BOOSTERS = {"x2": 0, "x3": 0, "x10": 0}
PLAYER_ACTIVE_BOOSTERS = []

BOOSTER_PRICES = {"x2": 50, "x3": 100, "x10": 300}
