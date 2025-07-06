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
ADDITIONAL_RADIUS = 15  # прибавляется при слиянии шариков
ACTIVE_BALL_Y = 100

BASKET_HORIZONTAL_MARGIN = 0.05  # 5% от ширины экрана
BASKET_BOTTOM_MARGIN = 0.05      # 5% от высоты экрана
BASKET_HEIGHT_RATIO = 0.4        # корзинка занимает 40% высоты экрана

BALL_IS_IMAGE = True  # если True, то для шаров используются картинки, иначе – цвета

# Задаём словарь для шаров: радиусы 15, 30, 45, ..., 375.
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

# Пути к звуковым файлам (файлы должны находиться либо в корневой папке, либо в указанном каталоге)
MERGE_SOUND_FILE = "sounds\\merge_sound.wav"
COLLISION_SOUND_FILE = ""
BUTTON_CLICK_SOUND_FILE = "sounds\\button_click.wav"

BACKGROUND_IMAGE_FILE = None  # Например, "background.png"
BG_COLOR = pygame.Color('white')

# Глобальная громкость для звуковых эффектов (от 0.0 до 1.0)
SOUND_VOLUME = 1.0
