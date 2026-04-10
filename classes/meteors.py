import pygame
import math
import random  # Added for random.choice
from settings_manager import current_settings  # Import current_settings

from .constants import WIDTH, HEIGHT


class Meteors(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 1
        self.direction_y = 1
        self.angle = 0
        self.speed = 2

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        if self.rect.bottom >= HEIGHT + 50 or self.rect.right >= WIDTH + 50:
            self.kill()

        self.angle = (self.angle - 1) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Meteors2(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 0
        self.direction_y = 1
        self.angle = 0
        self.speed = 2

    def update(self):
        self.rect.y += self.speed * self.direction_y

        if self.rect.bottom >= HEIGHT + 300:
            self.kill()

        self.angle = (self.angle - 1) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackHole(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 0
        self.direction_y = 1
        self.angle = 0
        self.speed = 2
        self.sound_effect = pygame.mixer.Sound("game_sounds/damage/black_hole.mp3")
        self.sound_effect.set_volume(
            current_settings["sound_effects"]
        )  # Changed to current_settings

    def update(self):
        self.rect.y += self.speed * self.direction_y

        if self.rect.bottom >= HEIGHT + 300:
            self.kill()

        self.angle = (self.angle - 1) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Wormhole(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 1
        self.angle = 0
        self.speed = 1
        self.amplitude = 50  # For sine wave movement
        self.frequency = 0.02  # For sine wave movement
        self.initial_x = x
        self.sound_effect = pygame.mixer.Sound(
            "game_sounds/refill/double_refill.mp3"
        )  # Placeholder for a teleport sound
        self.sound_effect.set_volume(
            current_settings["sound_effects"]
        )  # Changed to current_settings

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x = self.initial_x + self.amplitude * math.sin(
            pygame.time.get_ticks() * self.frequency
        )

        if self.rect.top > HEIGHT:
            self.kill()

        self.angle = (self.angle + 2) % 360  # Rotate wormhole
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
