import pygame
from settings_manager import current_settings  # Import current_settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=10):
        super().__init__()
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 10
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, -self.speed)

        if self.rect.bottom < 0:
            self.kill()
