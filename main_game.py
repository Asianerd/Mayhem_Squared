import math
import random
from enum import Enum
import pygame.rect

import bullet
import dependencies
import drop
import enemy


class SkillType(Enum):
    NoSkill = 0
    Rapid = 1
    Triple = 2
    Circle = 3
    Homing = 4
    Explosive = 5
    Railgun = 6


bullets = []
enemies = []
drops = []

fire_rate = dependencies.GameValue(0, 30, 1)
player = pygame.rect.Rect(400, 400, 50, 50)
coins = 0
speed = 10
active_skill: SkillType = SkillType.NoSkill
skill_age = dependencies.GameValue(1200, 1200, 1)

screen_shake = dependencies.GameValue(0, 30, 1)
screen_shake_strength = 50

screen_offset = [0, 0]


def screen_shake_handler(s):
    global screen_shake, screen_shake_strength
    screen_shake_strength = s
    screen_shake.affect_value(1)


def screen_offset_handler(v):
    global screen_offset
    screen_offset = v


def init(screen_size):
    drop.init()


def player_movement(inputs):
    vel = [0, 0]
    for index, x in enumerate([
        pygame.K_w,
        pygame.K_a,
        pygame.K_s,
        pygame.K_d,
    ]):
        if inputs[x][1]:
            vel[0] += [0, -1, 0, 1][index]
            vel[1] += [-1, 0, 1, 0][index]
    vel = dependencies.normalize(vel)
    vel[0] *= speed
    vel[1] *= speed
    player.x += vel[0]
    player.y += vel[1]


def drop_handler(d):
    drops.append(d)


def skill_handler(t: SkillType):
    global active_skill
    active_skill = t
    skill_age.affect_value(0)


def coin_handler(amount="check"):  # either "check" or an int
    global coins
    if amount == "check":
        return coins
    else:
        coins += amount


def update(inputs, mouse_pos, mouse_pressed, screen_size, scene_handler):
    global bullets, enemies, drops, active_skill, screen_offset
    player_movement(inputs)

    screen_offset = dependencies.lerp_vector2(screen_offset, [0, 0], 0.2)

    if screen_shake.percent() > 0:
        screen_shake.regen(-1)

    skill_age.regen()
    if skill_age.percent() >= 1:
        active_skill = SkillType.NoSkill

    fire_rate.regen()
    if mouse_pressed and (fire_rate.percent() >= 1):
        d = math.atan2(mouse_pos[1] - player.y - 25, mouse_pos[0] - player.x - 25)
        s = 5
        match active_skill:
            case SkillType.Rapid:
                fire_rate.affect_value(0.8)
                bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d, 5))
            case SkillType.Triple:
                fire_rate.affect_value(0)
                for i in range(3):
                    bullets.append(bullet.Bullet([player.x + 25, player.y + 25], float(d) + (float(i) * float(0.2)) - 0.2, 5))
            case SkillType.Circle:
                s = 0
                fire_rate.affect_value(0)
                for i in range(10):
                    bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d + (math.pi * i * 0.2), 5))
            case SkillType.Homing:
                fire_rate.affect_value(0)
                bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d, 5, 1))
            case SkillType.Explosive:
                s = 10
                fire_rate.affect_value(-3)
                bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d, 5, 2))
            case SkillType.Railgun:
                s = 20
                fire_rate.affect_value(-3)
                bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d, 5, 3))
            case _:
                fire_rate.affect_value(0)
                bullets.append(bullet.Bullet([player.x + 25, player.y + 25], d, 5))
        screen_offset_handler(dependencies.vector_multiply([
            math.cos(d + math.pi),
            math.sin(d + math.pi)
        ], s))

    if inputs[pygame.K_r][1]:
        enemies.append(enemy.Enemy(list(mouse_pos)))

    if inputs[pygame.K_e][0]:
        skill_handler(SkillType.Explosive)

    for x in bullets:
        x.update(enemies, screen_shake_handler)
    for x in enemies:
        x.update(player)
    for x in drops:
        x.update(player)
    [x.pickup(coin_handler, skill_handler) for x in drops if x.dead]
    drops = [x for x in drops if not x.dead]
    [x.on_death(drop_handler) for x in enemies if x.health.percent() <= 0]
    enemies = [x for x in enemies if x.health.percent() > 0]
    bullets = [x for x in bullets if x.age.percent() < 1]


def draw(window, font: pygame.font.Font, offset):
    offset = dependencies.vector_add(
        [(screen_shake.percent()) * random.randint(-screen_shake_strength, screen_shake_strength) for i in range(2)],
        offset)
    offset = dependencies.vector_add(screen_offset, offset)

    pygame.draw.rect(window, (100, 100, 255), [
        player[0] + offset[0],
        player[1] + offset[1],
        player[2], player[3]
    ])
    for x in bullets:
        x.draw(window, font, offset)
    for x in enemies:
        x.draw(window, offset)
    for x in drops:
        x.draw(window, offset)

    r = font.render(f"Coins : {coins}", True, (255, 255, 255))
    window.blit(r, (0, 0))
