import sys, argparse, pygame
from config import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, BG_COLOR
from scene_manager import SceneManager
from scenes.main_menu import MainMenuScene

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--window_width", type=int, default=DEFAULT_WINDOW_WIDTH)
    parser.add_argument("--window_height", type=int, default=DEFAULT_WINDOW_HEIGHT)
    args = parser.parse_args()
    w, h = args.window_width, args.window_height
    if w < MIN_WINDOW_WIDTH: w = MIN_WINDOW_WIDTH
    if h < MIN_WINDOW_HEIGHT: h = MIN_WINDOW_HEIGHT
    if w > MAX_WINDOW_WIDTH: w = MAX_WINDOW_WIDTH
    if h > MAX_WINDOW_HEIGHT: h = MAX_WINDOW_HEIGHT
    return w, h

def main():
    pygame.init()
    clock = pygame.time.Clock()
    window_width, window_height = parse_args()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Любимая игра дальтоника")
    manager = SceneManager(MainMenuScene(None, (window_width, window_height)))
    manager.current_scene.manager = manager
    running = True
    while running:
        dt = clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        manager.handle_events(events)
        manager.update(dt)
        manager.render(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
