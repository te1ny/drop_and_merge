import pygame
from config import BASKET_HORIZONTAL_MARGIN, BASKET_BOTTOM_MARGIN, BASKET_HEIGHT_RATIO

class Basket:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.horiz_margin = screen_width * BASKET_HORIZONTAL_MARGIN
        self.bottom_margin = screen_height * BASKET_BOTTOM_MARGIN
        self.width = screen_width - 2 * self.horiz_margin
        self.height = screen_height * BASKET_HEIGHT_RATIO
        # Основной прямоугольник корзинки (верх остаётся открытым)
        self.rect = pygame.Rect(self.horiz_margin, 
                                screen_height - self.bottom_margin - self.height, 
                                self.width, self.height)
        # ЛЕВАЯ граница – от левого края экрана до basket.rect.left, вертикально от rect.top до rect.bottom
        self.left_boundary = pygame.Rect(0, self.rect.top, self.rect.left, self.rect.height)
        # ПРАВАЯ граница – от basket.rect.right до правого края экрана, вертикально — как у basket.rect
        self.right_boundary = pygame.Rect(self.rect.right, self.rect.top, 
                                          screen_width - self.rect.right, self.rect.height)
        # НИЖНЯЯ граница – растянута по всей ширине экрана, от basket.rect.bottom до нижнего края экрана
        self.bottom_boundary = pygame.Rect(0, self.rect.bottom, screen_width, screen_height - self.rect.bottom)

    def draw(self, screen):
        color = pygame.Color('black')
        pygame.draw.rect(screen, color, self.left_boundary)
        pygame.draw.rect(screen, color, self.right_boundary)
        pygame.draw.rect(screen, color, self.bottom_boundary)
        # Рисуем контур корзинки (верхняя сторона не рисуется – она остаётся открытой)
        pygame.draw.line(screen, color, self.rect.topleft, self.rect.bottomleft, 2)
        pygame.draw.line(screen, color, self.rect.topright, self.rect.bottomright, 2)
        pygame.draw.line(screen, color, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), 2)
