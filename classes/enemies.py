import pygame
import random
from settings_manager import current_settings  # Import current_settings

from .constants import WIDTH, HEIGHT, ENEMY_FORCE


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y, image, diff_settings):
        super().__init__()
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4 * diff_settings["enemy_speed_multiplier"]
        self.direction = random.choice([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def update(self, enemy_group, diff_settings):
        dx, dy = self.direction
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.left < 5:
            self.rect.left = 5
            self.direction = random.choice([(1, 0), (0, -1), (0, 1), (1, -1), (1, 1)])
        elif self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
            self.direction = random.choice(
                [(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)]
            )

        if self.rect.top < 5:
            self.rect.top = 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1)])
        elif self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
            self.direction = random.choice(
                [(1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)]
            )

        collided_with = pygame.sprite.spritecollide(self, enemy_group, False)
        for other_enemy in collided_with:
            if other_enemy != self:
                distance_vec = pygame.math.Vector2(
                    other_enemy.rect.center
                ) - pygame.math.Vector2(self.rect.center)
                distance = distance_vec.length()
                angle = distance_vec.angle_to(pygame.math.Vector2(1, 0))

                repel_vec = pygame.math.Vector2(1, 0).rotate(angle)
                repel_vec *= 1 - (distance / (self.rect.width + other_enemy.rect.width))
                repel_vec *= ENEMY_FORCE

                self_dir = pygame.math.Vector2(self.direction)
                other_dir = pygame.math.Vector2(other_enemy.direction)

                if distance != 0:
                    new_dir = self_dir.reflect(distance_vec).normalize()
                    other_new_dir = other_dir.reflect(-distance_vec).normalize()

                    self.direction = new_dir.x, new_dir.y
                    other_enemy.direction = other_new_dir.x, other_new_dir.y

                self.rect.move_ip(-repel_vec.x, -repel_vec.y)
                other_enemy.rect.move_ip(repel_vec.x, repel_vec.y)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y, image, diff_settings):
        super().__init__()
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4 * diff_settings["enemy_speed_multiplier"]
        self.direction = random.choice([(-1, 0), (1, 0)])
        self.shoot_timer = 0
        self.shots_fired = 0
        self.base_shoot_timer = 60  # Base value for Enemy2 shoot timer

    def update(self, enemy_group, enemy_bullets_group, player, diff_settings):
        if self.shots_fired < 10:
            dx, dy = self.direction
            self.rect.x += dx * self.speed
            self.rect.y = max(self.rect.y, 5)

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction = (1, 0)
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction = (-1, 0)

            collided_with = pygame.sprite.spritecollide(self, enemy_group, False)
            for other_enemy in collided_with:
                if other_enemy != self:
                    distance_vec = pygame.math.Vector2(
                        other_enemy.rect.center
                    ) - pygame.math.Vector2(self.rect.center)
                    distance = distance_vec.length()
                    angle = distance_vec.angle_to(pygame.math.Vector2(1, 0))

                    repel_vec = pygame.math.Vector2(1, 0).rotate(angle)
                    repel_vec *= 1 - (
                        distance / (self.rect.width + other_enemy.rect.width)
                    )
                    repel_vec *= ENEMY_FORCE

                    self_dir = pygame.math.Vector2(self.direction)
                    other_dir = pygame.math.Vector2(other_enemy.direction)

                    if distance != 0:
                        new_dir = self_dir.reflect(distance_vec).normalize()
                        other_new_dir = other_dir.reflect(-distance_vec).normalize()

                        self.direction = new_dir.x, new_dir.y
                        other_enemy.direction = other_new_dir.x, other_new_dir.y

                    self.rect.move_ip(-repel_vec.x, -repel_vec.y)
                    other_enemy.rect.move_ip(repel_vec.x, repel_vec.y)

            self.shoot_timer += 1
            if (
                self.shoot_timer
                >= self.base_shoot_timer * diff_settings["boss_shoot_timer_multiplier"]
            ):
                bullet = Enemy2Bullet(self.rect.centerx, self.rect.bottom)
                enemy_bullets_group.add(bullet)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            self.speed = (
                10 * diff_settings["enemy_speed_multiplier"]
            )  # Speed up when chasing player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed


class Enemy2Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        if image is None:
            self.image = pygame.image.load("images/bullets/bullet2.png").convert_alpha()
        elif isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 8

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
