import pygame
from config import *
class Card:
    instances = []
    guesses = []
    correct = []

    def __init__(self, x, y, image, set_id, row):
        self.x = x
        self.y = y
        self.image = image
        self.set_id = set_id
        self.row = row
        self.revealed = False
        self.alpha = 0
        self.fade_direction = 0
        self.rect = image.get_rect(topleft=(x, y))
        Card.instances.append(self)

    def start_fade_in(self):
        self.fade_direction = 1

    def start_fade_out(self):
        self.fade_direction = -1

    def update(self):
        if self.fade_direction != 0:
            self.alpha += self.fade_direction * FADE_SPEED
            self.alpha = max(0, min(255, self.alpha))
            if self.alpha in (0, 255):
                self.fade_direction = 0
                self.revealed = (self.alpha == 255)

    def draw(self, surface):
        if self.alpha > 0:
            temp_img = self.image.copy()
            temp_img.set_alpha(self.alpha)
            surface.blit(temp_img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, (50, 50, 50), self.rect, border_radius=10)
            pygame.draw.rect(surface, (200, 200, 200), self.rect, width=2, border_radius=10)
