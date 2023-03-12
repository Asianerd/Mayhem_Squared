import pygame
import dependencies
import math
from enum import Enum


class BulletType(Enum):
    Normal = 0
    Homing = 1
    Explosive = 2
    Railgun = 3


class Bullet:
    def __init__(self, p, d, s, t=0):
        self.pos = p
        self.direction = d
        self.speed = s
        self.damage = 20

        self.type = BulletType(t)

        self.speed *= 10 if self.type == BulletType.Railgun else 1
        self.damage *= 10 if self.type == BulletType.Railgun else 1
        self.damage *= 10 if self.type == BulletType.Explosive else 1

        self.age = dependencies.GameValue(0, 120, 1)

    def update(self, enemies, shake_handler):
        self.age.regen()

        if self.type == BulletType.Homing:
            if len(enemies) > 0:
                nearest = sorted(enemies, key=lambda x:math.sqrt(math.pow(x.pos[0] - self.pos[0], 2) + math.pow(x.pos[1] - self.pos[1], 2)))[0].pos
                self.direction = math.atan2(
                        nearest[1] - self.pos[1],
                        nearest[0] - self.pos[0]
                    )

                # self.direction = dependencies.lerp(
                #     0.1,
                #     self.direction,
                #     d
                # )
                # stupid bug
                # print(f"T :{round(math.atan2(nearest[1] - self.pos[1], nearest[0] - self.pos[0]), 2)}")
                # print(round(self.direction, 2))

        self.pos[0] += math.cos(self.direction) * self.speed
        self.pos[1] += math.sin(self.direction) * self.speed

        rect = pygame.rect.Rect(self.pos, [5, 5])

        for x in enemies:
            if rect.colliderect(x.rect):
                if self.type == BulletType.Explosive:
                    for i in [n for n in enemies if math.sqrt(math.pow(n.pos[0] - self.pos[0], 2) + math.pow(n.pos[1] - self.pos[1], 2)) < 200]:
                        i.health.i -= self.damage * (1 - (math.sqrt(math.pow(i.pos[0] - self.pos[0], 2) + math.pow(i.pos[1] - self.pos[1], 2)) / 200))
                        i.damage_flash = 5
                    shake_handler(50)
                else:
                    x.health.i -= self.damage
                    x.damage_flash = 5
                if self.type != BulletType.Railgun:
                    self.age.affect_value(1)
                    break

    def draw(self, window, font, offset):
        pygame.draw.circle(window, (255, 255, 255), [
            self.pos[0] + offset[0],
            self.pos[1] + offset[1]
        ], 5)
