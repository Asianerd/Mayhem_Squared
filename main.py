import pygame

pygame.init()

screen_size = [1000, 1000]
#screen_size = [100, 100]
window = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont('consolas', 30)
clock = pygame.time.Clock()
run = True

# i = ""
# for x in range(10):
#     i += "?"
#     print(font.size(i))

active_scene = 0
# 0 main menu
# 1 main game

mouse_pos = [0, 0]
mouse_pressed = False

inputs = {}
for i in [
    pygame.K_ESCAPE,

    pygame.K_w,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_r,
    pygame.K_e,
    pygame.K_LSHIFT,
    pygame.K_SPACE,
]:
    inputs[i] = [False, False, False]
    # [active, currently pressed, previously pressed]


def update_inputs():
    for x in inputs:
        inputs[x][2] = inputs[x][1]
        inputs[x][1] = pygame.key.get_pressed()[x]
        inputs[x][0] = inputs[x][1] and (not inputs[x][2])


def game_loop():
    global mouse_pos, mouse_pressed, run

    import main_menu
    import main_game

    main_menu.init(screen_size)
    main_game.init(screen_size)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0, 0, 0))
        update_inputs()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if inputs[pygame.K_ESCAPE][1]:
            run = False

        [main_menu, main_game][active_scene].update(inputs, mouse_pos, mouse_pressed, screen_size, change_scene)
        [main_menu, main_game][active_scene].draw(window, font, [0, 0])
        pygame.display.update()


def change_scene(s):
    global active_scene
    active_scene = s


if __name__ == "__main__":
    game_loop()
