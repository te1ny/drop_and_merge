import sys
import pygame

class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def go_to(self, scene):
        self.current_scene = scene

    def handle_events(self, events):
        self.current_scene.handle_events(events)

    def update(self, dt):
        self.current_scene.update(dt)

    def render(self, screen):
        self.current_scene.render(screen)
