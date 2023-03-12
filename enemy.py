import math
import random
import pygame
import dependencies
import drop


class Enemy:
    speed = 0

    def __init__(self, p):
        self.pos = p
        self.rect = pygame.rect.Rect(p, [50, 50])
        self.health = dependencies.GameValue(100, 100, 1)

        self.damage_flash = 0

    def update(self, player):
        d = math.atan2(
            player.y - self.pos[1],
            player.x - self.pos[0]
        )
        self.pos[0] += math.cos(d) * Enemy.speed
        self.pos[1] += math.sin(d) * Enemy.speed

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.damage_flash > 0:
            self.damage_flash -= 1

    def on_death(self, drop_func):
        drop_func(drop.Drop(self.rect.center, [drop.DropType.Coin, drop.DropType.Skill][random.randint(0, 10) > 9]))

    def draw(self, window, offset):
        pygame.draw.rect(window, (255, 100, 100) if (self.damage_flash == 0) else (255, 255, 255), [
            self.pos[0] + offset[0],
            self.pos[1] + offset[1],
            self.rect.width,
            self.rect.height
        ])