import random
import math
import pygame
from enum import Enum

import dependencies


class DropType(Enum):
    Coin = 0
    Skill = 1


def init():
    global skills
    from main_game import SkillType
    for x in SkillType:
        skills.append(x)


skills = []


class Drop:
    def __init__(self, p, t):
        # data is int if coins
        # data is SkillType if skill
        self.pos = [p[0], p[1]]
        self.rect = pygame.rect.Rect(self.pos, [10, 10])
        self.type = t
        if self.type == DropType.Coin:
            self.coin_amount = 1
        else:
            self.skill_type = skills[random.randint(0, len(skills) - 1)]

        self.follow = False
        self.dead = False

    def update(self, player_pos: pygame.rect.Rect):
        if dependencies.distance(player_pos, self.pos) < 100:
            self.follow = True
        if self.follow:
            d = math.atan2(player_pos.center[1] - self.pos[1], player_pos.center[0] - self.pos[0])
            self.pos = dependencies.vector_add(self.pos, dependencies.vector_multiply([
                math.cos(d),
                math.sin(d)
            ], 5))

        if dependencies.distance(player_pos.center, self.pos) < 10:
            self.dead = True

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self, window, offset):
        pygame.draw.rect(window, {
            DropType.Coin: (255, 215, 0),
            DropType.Skill: (100, 255, 100)
        }[self.type], [
            self.rect.x + offset[0],
            self.rect.y + offset[1],
            self.rect.width,
            self.rect.height
        ])

    def pickup(self, coin_func, skill_func):
        match self.type:
            case DropType.Coin:
                coin_func(self.coin_amount)
            case _:
                skill_func(self.skill_type)
