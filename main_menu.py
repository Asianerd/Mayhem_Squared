import pygame
import button

start_button = button.Button("Play", pygame.rect.Rect(0, 0, 200, 100), (0, 255, 0), (255, 255, 255))


def init(screen_size):
    start_button.rect.x = (screen_size[0] - start_button.rect.width) / 2
    start_button.rect.y = (screen_size[1] - start_button.rect.height) / 2


def update(inputs, mouse_pos, mouse_pressed, screen_size, scene_handler):
    start_button.update(mouse_pos, mouse_pressed)
    if start_button.active:
        scene_handler(1)


def draw(window, font, offset):
    start_button.draw(window, font, offset)
