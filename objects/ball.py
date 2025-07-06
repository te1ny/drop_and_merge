import pygame
import os
from config import BALL_IS_IMAGE

class Ball:
    def __init__(self, position, radius, is_image, ball_dict):
        self.position = list(position)
        self.velocity = [0, 0]
        self.radius = radius
        self.is_image = is_image
        self.ball_dict = ball_dict
        self.mass = self.radius ** 2
        self.update_image()

    def update_image(self):
        if self.radius in self.ball_dict:
            color_entry, path = self.ball_dict[self.radius]
        else:
            keys = sorted(self.ball_dict.keys())
            if keys:
                color_entry, path = self.ball_dict[keys[0]]
            else:
                color_entry, path = (pygame.Color('black'), None)

        if self.is_image:
            if path and os.path.exists(path):
                self.image = pygame.image.load(path)
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
                self.color = color_entry
            else:
                self.image = None
                self.color = color_entry
        else:
            self.image = None
            self.color = color_entry

        self.mass = self.radius ** 2

    def draw(self, screen):
        if self.is_image and self.image:
            rect = self.image.get_rect(center=(int(self.position[0]), int(self.position[1])))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

    def is_off_screen(self, screen_width, screen_height):
        if self.position[0] + self.radius < 0 or self.position[0] - self.radius > screen_width:
            return True

        if self.position[1] - self.radius > screen_height:
            return True

        return False
