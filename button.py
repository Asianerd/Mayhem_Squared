import pygame.draw


class Button:
    def __init__(self, text, rect, color, text_color):
        self.text = text
        self.rect = rect
        self.hovered = False
        self.is_pressed = False
        self.was_pressed = False
        self.active = False

        self.text_pos = [0, 0]

        self.color = color
        self.text_color = text_color

    def update(self, mouse_pos, mouse_pressed):
        self.hovered = self.rect.contains(mouse_pos, [1, 1])

        self.was_pressed = self.is_pressed
        if self.hovered:
            self.is_pressed = mouse_pressed

        self.active = self.is_pressed and (not self.was_pressed)

    def draw(self, window, font: pygame.font.Font, offset):
        self.text_pos = font.size(self.text)
        self.text_pos = [
            self.rect.x + ((self.rect.width - self.text_pos[0]) / 2),
            self.rect.y + ((self.rect.height - self.text_pos[1]) / 2)
        ]

        pygame.draw.rect(window, [x * ((0.5 if self.is_pressed else 1) if self.hovered else 0.9) for x in self.color], [
            self.rect.x + offset[0],
            self.rect.y + offset[1],
            self.rect.width,
            self.rect.height
        ])

        window.blit(
            font.render(self.text, True, self.text_color),
            [
                self.text_pos[0] + offset[0],
                self.text_pos[1] + offset[1]
            ]
        )

