import pygame
import random
import logging

from controls import move_player, move_player_with_joystick
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from functions import show_game_over, music_background, show_game_win

from classes.player import Player
from classes.bullets import Bullet
from classes.refill import HealthRefill, ExtraScore
from classes.explosions import Explosion, Explosion2
from classes.enemies import Enemy1
from classes.bosses import Boss1, Boss2, Boss3
from high_score_manager import load_high_scores, add_high_score
from settings_manager import current_settings, save_settings
from classes.ship_config import SHIPS_CONFIG

# --- Global Variables ---
game_initialized = False
screen = None
surface = None
clock = None

# Sprite Groups
explosions = None
explosions2 = None
bullets = None
enemy1_group = None
enemy2_group = None
boss1_group = None
boss2_group = None
boss3_group = None
bullet_refill_group = None
health_refill_group = None
double_refill_group = None
meteor_group = None
meteor2_group = None
extra_score_group = None
black_hole_group = None
unlimited_bullet_refill_group = None
fire_rate_upgrade_group = None
wormhole_group = None
enemy2_bullets = None
boss1_bullets = None
boss2_bullets = None
boss3_bullets = None

# Assets
background_img = None
background_img2 = None
background_img3 = None
background_img4 = None
explosion_images = []
explosion2_images = []
explosion3_images = []
enemy1_img = []
enemy2_img = []
boss1_img = None
boss2_img = None
boss3_img = None
health_refill_img = None
bullet_refill_img = None
double_refill_img = None
unlimited_bullet_refill_img = None
fire_rate_upgrade_img = None
meteor_imgs = []
meteor2_imgs = []
extra_score_img = None
black_hole_imgs = []
wormhole_img = None
life_bar_image = None
bullet_bar_image = None
player_image = None
ship_stats = None

# Game State
score = 0
hi_score = 0
player = None
player_life = 0
bullet_counter = 0
unlimited_bullets_active = False
unlimited_bullets_start_time = 0
fire_rate_upgraded_active = False
fire_rate_upgraded_start_time = 0
current_shoot_delay = SHOOT_DELAY
min_shoot_delay = 50
current_level_idx = 0
current_level_data = None
current_bg_image = None
current_bg_top = None
bg_y_shift = 0
boss1_spawned = False
boss2_spawned = False
boss3_spawned = False
boss1_health = 0
boss2_health = 0
boss3_health = 0
diff_settings = None

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

DIFFICULTY_SETTINGS = {
    "Easy": {
        "enemy_spawn_multiplier": 1.5,
        "meteor_spawn_multiplier": 1.2,
        "boss_health_multiplier": 0.8,
        "player_life_start": 300,
        "bullet_start": 300,
        "shoot_delay_base": 200,
        "enemy_speed_multiplier": 0.8,
        "boss_speed_multiplier": 0.8,
        "boss_shoot_timer_multiplier": 1.5,
    },
    "Normal": {
        "enemy_spawn_multiplier": 1.0,
        "meteor_spawn_multiplier": 1.0,
        "boss_health_multiplier": 1.0,
        "player_life_start": 200,
        "bullet_start": 200,
        "shoot_delay_base": SHOOT_DELAY,
        "enemy_speed_multiplier": 1.0,
        "boss_speed_multiplier": 1.0,
        "boss_shoot_timer_multiplier": 1.0,
    },
    "Hard": {
        "enemy_spawn_multiplier": 0.7,
        "meteor_spawn_multiplier": 0.8,
        "boss_health_multiplier": 1.2,
        "player_life_start": 100,
        "bullet_start": 100,
        "shoot_delay_base": 100,
        "enemy_speed_multiplier": 1.2,
        "boss_speed_multiplier": 1.2,
        "boss_shoot_timer_multiplier": 0.7,
    },
}

LEVELS = []


def initialize_game():
    global \
        game_initialized, \
        screen, \
        surface, \
        clock, \
        explosions, \
        explosions2, \
        bullets, \
        enemy1_group, \
        enemy2_group, \
        boss1_group, \
        boss2_group, \
        boss3_group, \
        bullet_refill_group, \
        health_refill_group, \
        double_refill_group, \
        meteor_group, \
        meteor2_group, \
        extra_score_group, \
        black_hole_group, \
        unlimited_bullet_refill_group, \
        fire_rate_upgrade_group, \
        wormhole_group, \
        enemy2_bullets, \
        boss1_bullets, \
        boss2_bullets, \
        boss3_bullets, \
        background_img, \
        background_img2, \
        background_img3, \
        background_img4, \
        explosion_images, \
        explosion2_images, \
        explosion3_images, \
        enemy1_img, \
        enemy2_img, \
        boss1_img, \
        boss2_img, \
        boss3_img, \
        health_refill_img, \
        bullet_refill_img, \
        double_refill_img, \
        unlimited_bullet_refill_img, \
        fire_rate_upgrade_img, \
        meteor_imgs, \
        meteor2_imgs, \
        extra_score_img, \
        black_hole_imgs, \
        wormhole_img, \
        life_bar_image, \
        bullet_bar_image, \
        player_image, \
        ship_stats, \
        LEVELS

    if game_initialized:
        return

    pygame.init()
    music_background()
    pygame.mixer.music.set_volume(current_settings["music_volume"])
    # Surface used for some effects, keep it but remove redundant set_mode
    surface = pygame.Surface((WIDTH, HEIGHT))
    pygame.display.set_caption("Cosmic Heat")
    clock = pygame.time.Clock()

    # Sprite Groups
    explosions = pygame.sprite.Group()
    explosions2 = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy1_group = pygame.sprite.Group()
    enemy2_group = pygame.sprite.Group()
    boss1_group = pygame.sprite.Group()
    boss2_group = pygame.sprite.Group()
    boss3_group = pygame.sprite.Group()
    bullet_refill_group = pygame.sprite.Group()
    health_refill_group = pygame.sprite.Group()
    double_refill_group = pygame.sprite.Group()
    meteor_group = pygame.sprite.Group()
    meteor2_group = pygame.sprite.Group()
    extra_score_group = pygame.sprite.Group()
    black_hole_group = pygame.sprite.Group()
    unlimited_bullet_refill_group = pygame.sprite.Group()
    fire_rate_upgrade_group = pygame.sprite.Group()
    wormhole_group = pygame.sprite.Group()
    enemy2_bullets = pygame.sprite.Group()
    boss1_bullets = pygame.sprite.Group()
    boss2_bullets = pygame.sprite.Group()
    boss3_bullets = pygame.sprite.Group()

    # Load Assets
    background_img = pygame.transform.scale(
        pygame.image.load("images/bg/background.jpg").convert(), (WIDTH, HEIGHT)
    )
    background_img2 = pygame.transform.scale(
        pygame.image.load("images/bg/background2.png").convert(), (WIDTH, HEIGHT)
    )
    background_img3 = pygame.transform.scale(
        pygame.image.load("images/bg/background3.png").convert(), (WIDTH, HEIGHT)
    )
    background_img4 = pygame.transform.scale(
        pygame.image.load("images/bg/background4.png").convert(), (WIDTH, HEIGHT)
    )

    life_bar_image = pygame.image.load("images/life_bar.png").convert_alpha()
    bullet_bar_image = pygame.image.load("images/bullet_bar.png").convert_alpha()

    # Load Equipped Ship
    equipped_ship_name = current_settings.get("equipped_ship", "Standard")
    ship_stats = SHIPS_CONFIG.get(equipped_ship_name, SHIPS_CONFIG["Standard"])
    player_image = pygame.image.load(ship_stats["image_path"]).convert_alpha()
    player_image = pygame.transform.scale(
        player_image, (100, 100)
    )  # Ensure standard size

    explosion_images = [
        pygame.image.load(f"images/explosion/explosion{i}.png").convert_alpha()
        for i in range(8)
    ]
    explosion2_images = [
        pygame.image.load(f"images/explosion2/explosion{i}.png").convert_alpha()
        for i in range(18)
    ]
    explosion3_images = [
        pygame.image.load(f"images/explosion3/explosion{i}.png").convert_alpha()
        for i in range(18)
    ]

    enemy1_img = [
        pygame.image.load(f"images/enemy/enemy1_{i}.png").convert_alpha()
        for i in range(1, 4)
    ]
    enemy2_img = [
        pygame.image.load(f"images/enemy/enemy2_{i}.png").convert_alpha()
        for i in range(1, 3)
    ]
    boss1_img = pygame.image.load("images/boss/boss1.png").convert_alpha()
    boss2_img = pygame.image.load("images/boss/boss2_1.png").convert_alpha()
    boss3_img = pygame.image.load("images/boss/boss3.png").convert_alpha()

    health_refill_img = pygame.image.load(
        "images/refill/health_refill.png"
    ).convert_alpha()
    bullet_refill_img = pygame.image.load(
        "images/refill/bullet_refill.png"
    ).convert_alpha()
    double_refill_img = pygame.image.load(
        "images/refill/double_refill.png"
    ).convert_alpha()
    unlimited_bullet_refill_img = pygame.image.load(
        "images/refill/xxx.png"
    ).convert_alpha()
    fire_rate_upgrade_img = pygame.image.load("images/refill/xxx.png").convert_alpha()

    meteor_imgs = [
        pygame.image.load(f"images/meteors/meteor_{i}.png").convert_alpha()
        for i in range(1, 5)
    ]
    meteor2_imgs = [
        pygame.image.load(f"images/meteors/meteor2_{i}.png").convert_alpha()
        for i in range(1, 5)
    ]
    extra_score_img = pygame.image.load("images/score/score_coin.png").convert_alpha()
    black_hole_imgs = [
        pygame.image.load("images/hole/black_hole.png").convert_alpha(),
        pygame.image.load("images/hole/black_hole2.png").convert_alpha(),
    ]
    wormhole_img = black_hole_imgs[0]

    LEVELS = [
        {
            "level_number": 1,
            "score_to_next_level": 3000,
            "background_img": background_img,
            "enemy1_base_spawn_rate": 120,
            "enemy2_base_spawn_rate": 0,
            "meteor_base_spawn_rate": 100,
            "meteor2_base_spawn_rate": 90,
            "black_hole_base_spawn_rate": 0,
            "wormhole_base_spawn_rate": 0,
            "boss_type": None,
        },
        {
            "level_number": 2,
            "score_to_next_level": 10000,
            "background_img": background_img2,
            "enemy1_base_spawn_rate": 100,
            "enemy2_base_spawn_rate": 40,
            "meteor_base_spawn_rate": 80,
            "meteor2_base_spawn_rate": 70,
            "black_hole_base_spawn_rate": 500,
            "wormhole_base_spawn_rate": 800,
            "boss_type": Boss1,
        },
        {
            "level_number": 3,
            "score_to_next_level": 15000,
            "background_img": background_img3,
            "enemy1_base_spawn_rate": 80,
            "enemy2_base_spawn_rate": 30,
            "meteor_base_spawn_rate": 60,
            "meteor2_base_spawn_rate": 50,
            "black_hole_base_spawn_rate": 400,
            "wormhole_base_spawn_rate": 600,
            "boss_type": Boss2,
        },
        {
            "level_number": 4,
            "score_to_next_level": 25000,
            "background_img": background_img4,
            "enemy1_base_spawn_rate": 60,
            "enemy2_base_spawn_rate": 20,
            "meteor_base_spawn_rate": 40,
            "meteor2_base_spawn_rate": 30,
            "black_hole_base_spawn_rate": 300,
            "wormhole_base_spawn_rate": 400,
            "boss_type": Boss3,
        },
    ]
    game_initialized = True


def reset_game_state():
    global \
        score, \
        hi_score, \
        player, \
        player_life, \
        bullet_counter, \
        unlimited_bullets_active, \
        unlimited_bullets_start_time, \
        fire_rate_upgraded_active, \
        fire_rate_upgraded_start_time, \
        current_shoot_delay, \
        min_shoot_delay, \
        current_level_idx, \
        current_level_data, \
        current_bg_image, \
        current_bg_top, \
        bg_y_shift, \
        boss1_spawned, \
        boss2_spawned, \
        boss3_spawned, \
        boss1_health, \
        boss2_health, \
        boss3_health, \
        diff_settings, \
        player_image, \
        ship_stats

    diff_settings = DIFFICULTY_SETTINGS[current_settings["difficulty"]]
    score = 0
    scores = load_high_scores()
    hi_score = scores[0]["score"] if scores else 0

    player = Player(player_image, ship_stats)
    player.rect.topleft = initial_player_pos
    # Apply ship health multiplier
    player_life = int(diff_settings["player_life_start"] * ship_stats["health_mult"])
    bullet_counter = diff_settings["bullet_start"]

    unlimited_bullets_active = False
    fire_rate_upgraded_active = False
    # Apply ship fire rate multiplier
    current_shoot_delay = int(
        diff_settings["shoot_delay_base"] * ship_stats["fire_rate_mult"]
    )

    current_level_idx = 0
    current_level_data = LEVELS[current_level_idx]
    current_bg_image = current_level_data["background_img"]
    current_bg_top = current_level_data["background_img"].copy()
    bg_y_shift = 0

    boss1_spawned = boss2_spawned = boss3_spawned = False
    boss1_health = int(150 * diff_settings["boss_health_multiplier"])
    boss2_health = int(150 * diff_settings["boss_health_multiplier"])
    boss3_health = int(200 * diff_settings["boss_health_multiplier"])

    for group in [
        bullets,
        bullet_refill_group,
        health_refill_group,
        double_refill_group,
        extra_score_group,
        black_hole_group,
        unlimited_bullet_refill_group,
        fire_rate_upgrade_group,
        wormhole_group,
        meteor_group,
        meteor2_group,
        enemy1_group,
        enemy2_group,
        boss1_group,
        boss2_group,
        boss3_group,
        explosions,
        explosions2,
        enemy2_bullets,
        boss1_bullets,
        boss2_bullets,
        boss3_bullets,
    ]:
        group.empty()


def in_game_menu(screen_obj):
    menu_font = pygame.font.SysFont("Impact", 40)
    options = ["Resume", "Restart", "Back to Menu"]
    selected_option = 0
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    return "resume"
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                if event.key == pygame.K_RETURN:
                    return ["resume", "restart", "menu"][selected_option]

        screen_obj.blit(overlay, (0, 0))
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            text = menu_font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 70))
            screen_obj.blit(text, rect)
        pygame.display.flip()
        clock.tick(FPS)


def run_game(screen_obj):
    global \
        score, \
        hi_score, \
        player_life, \
        bullet_counter, \
        unlimited_bullets_active, \
        unlimited_bullets_start_time, \
        fire_rate_upgraded_active, \
        fire_rate_upgraded_start_time, \
        current_shoot_delay, \
        current_level_idx, \
        current_level_data, \
        current_bg_image, \
        current_bg_top, \
        bg_y_shift, \
        boss1_spawned, \
        boss2_spawned, \
        boss3_spawned, \
        boss1_health, \
        boss2_health, \
        boss3_health, \
        screen

    logging.info("Starting run_game")
    try:
        initialize_game()
        screen = screen_obj
        reset_game_state()
        logging.info("Game state reset")

        running = True
        paused = False
        is_shooting = False
        last_shot_time = 0

        joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
        if joystick:
            joystick.init()
            logging.info("Joystick initialized in run_game")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not paused:
                        is_shooting = True
                    if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                        paused = not paused
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        is_shooting = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        is_shooting = True
                    if event.button == 7:
                        paused = not paused
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        is_shooting = False

            if paused:
                action = in_game_menu(screen)
                if action == "resume":
                    paused = False
                else:
                    return action

            # Player Movement
            if not paused:
                if joystick:
                    move_player_with_joystick(joystick, player)
                else:
                    move_player(pygame.key.get_pressed(), player)

            # Shooting Logic
            now = pygame.time.get_ticks()
            if is_shooting and not paused and now - last_shot_time > current_shoot_delay:
                if bullet_counter > 0 or unlimited_bullets_active:
                    f_mode = ship_stats.get("fire_mode", "single")
                    b_img = ship_stats.get("bullet_image", "images/bullets/bullet1.png")

                    if f_mode == "single":
                        bullets.add(Bullet(player.rect.centerx, player.rect.top, b_img))
                    elif f_mode == "double":
                        bullets.add(Bullet(player.rect.left + 20, player.rect.top, b_img))
                        bullets.add(Bullet(player.rect.right - 20, player.rect.top, b_img))
                    elif f_mode == "triple":
                        bullets.add(Bullet(player.rect.centerx, player.rect.top, b_img))
                        bullets.add(
                            Bullet(player.rect.left + 10, player.rect.top + 20, b_img)
                        )
                        bullets.add(
                            Bullet(player.rect.right - 10, player.rect.top + 20, b_img)
                        )

                    if not unlimited_bullets_active:
                        bullet_counter -= (
                            1 if f_mode == "single" else 2 if f_mode == "double" else 3
                        )
                        if bullet_counter < 0:
                            bullet_counter = 0
                    last_shot_time = now

            # Power-up Timers
            if unlimited_bullets_active and now - unlimited_bullets_start_time > 5000:
                unlimited_bullets_active = False
            if fire_rate_upgraded_active and now - fire_rate_upgraded_start_time > 5000:
                fire_rate_upgraded_active = False
                current_shoot_delay = diff_settings["shoot_delay_base"]

            # Background Scrolling
            screen.fill((0, 0, 0))  # Clear the screen before drawing
            screen.blit(current_bg_image, (0, bg_y_shift))
            screen.blit(current_bg_top, (0, bg_y_shift - HEIGHT))
            bg_y_shift += 1
            if bg_y_shift >= HEIGHT:
                bg_y_shift = 0

            # Sprite Updates
            bullets.update()
            enemy1_group.update(enemy1_group, diff_settings)
            enemy2_group.update(enemy2_group, enemy2_bullets, player, diff_settings)
            enemy2_bullets.update()
            boss1_group.update(boss1_bullets, player, diff_settings)
            boss1_bullets.update()
            boss2_group.update(boss2_bullets, player, diff_settings)
            boss2_bullets.update()
            boss3_group.update(boss3_bullets, player, diff_settings)
            boss3_bullets.update()
            meteor_group.update()
            meteor2_group.update()
            black_hole_group.update()
            wormhole_group.update()
            bullet_refill_group.update()
            health_refill_group.update()
            double_refill_group.update()
            extra_score_group.update()
            unlimited_bullet_refill_group.update()
            fire_rate_upgrade_group.update()
            explosions.update()
            explosions2.update()

            # --- Collisions ---
            # Bullet hits Enemy
            for group in [enemy1_group, enemy2_group]:
                hits = pygame.sprite.groupcollide(group, bullets, True, True)
                for hit in hits:
                    score += 100
                    explosions.add(Explosion(hit.rect.center, explosion_images))
                    if random.randint(0, 10) == 0:
                        health_refill_group.add(
                            HealthRefill(hit.rect.x, hit.rect.y, health_refill_img)
                        )

            # Bullet hits Boss
            # Boss 1
            hits1 = pygame.sprite.groupcollide(boss1_group, bullets, False, True)
            for hit in hits1:
                boss1_health -= 10
                if boss1_health <= 0:
                    score += 5000
                    explosions2.add(Explosion2(hit.rect.center, explosion2_images))
                    hit.kill()
                    # Update boss kill count and check unlocks
                    current_settings["total_boss_kills"] += 1
                    for ship_name, info in SHIPS_CONFIG.items():
                        if (
                            current_settings["total_boss_kills"] >= info["requirement"]
                            and ship_name not in current_settings["unlocked_ships"]
                        ):
                            current_settings["unlocked_ships"].append(ship_name)
                    save_settings(current_settings)

            # Boss 2
            hits2 = pygame.sprite.groupcollide(boss2_group, bullets, False, True)
            for hit in hits2:
                boss2_health -= 10
                if boss2_health <= 0:
                    score += 5000
                    explosions2.add(Explosion2(hit.rect.center, explosion2_images))
                    hit.kill()
                    # Update boss kill count and check unlocks
                    current_settings["total_boss_kills"] += 1
                    for ship_name, info in SHIPS_CONFIG.items():
                        if (
                            current_settings["total_boss_kills"] >= info["requirement"]
                            and ship_name not in current_settings["unlocked_ships"]
                        ):
                            current_settings["unlocked_ships"].append(ship_name)
                    save_settings(current_settings)

            # Boss 3
            hits3 = pygame.sprite.groupcollide(boss3_group, bullets, False, True)
            for hit in hits3:
                boss3_health -= 10
                if boss3_health <= 0:
                    score += 5000
                    explosions2.add(Explosion2(hit.rect.center, explosion2_images))
                    hit.kill()
                    # Update boss kill count and check unlocks
                    current_settings["total_boss_kills"] += 1
                    for ship_name, info in SHIPS_CONFIG.items():
                        if (
                            current_settings["total_boss_kills"] >= info["requirement"]
                            and ship_name not in current_settings["unlocked_ships"]
                        ):
                            current_settings["unlocked_ships"].append(ship_name)
                    save_settings(current_settings)

            # Player hits Enemy/Meteor/Hazard
            for group in [
                enemy1_group,
                enemy2_group,
                meteor_group,
                meteor2_group,
                enemy2_bullets,
                boss1_bullets,
                boss2_bullets,
                boss3_bullets,
            ]:
                if pygame.sprite.spritecollide(player, group, True):
                    player_life -= 20
                    explosions.add(Explosion(player.rect.center, explosion_images))

            # Player hits Refills
            for group, effect in [
                (health_refill_group, "health"),
                (bullet_refill_group, "bullets"),
                (extra_score_group, "score"),
                (unlimited_bullet_refill_group, "unlimited"),
                (fire_rate_upgrade_group, "firerate"),
            ]:
                hits = pygame.sprite.spritecollide(player, group, True)
                for hit in hits:
                    hit.sound_effect.play()
                    if effect == "health":
                        player_life = min(
                            player_life + 50, diff_settings["player_life_start"]
                        )
                    elif effect == "bullets":
                        bullet_counter += 50
                    elif effect == "score":
                        score += 500
                    elif effect == "unlimited":
                        unlimited_bullets_active = True
                        unlimited_bullets_start_time = now
                    elif effect == "firerate":
                        fire_rate_upgraded_active = True
                        fire_rate_upgraded_start_time = now
                        current_shoot_delay = 50

            # Spawning logic (Level based)
            if random.randint(0, 1000) < 5:  # Random extra score
                extra_score_group.add(
                    ExtraScore(random.randint(0, WIDTH), -50, extra_score_img)
                )

            if (
                current_level_data["enemy1_base_spawn_rate"] > 0
                and random.randint(
                    0,
                    int(
                        current_level_data["enemy1_base_spawn_rate"]
                        * diff_settings["enemy_spawn_multiplier"]
                    ),
                )
                == 0
            ):
                enemy1_group.add(
                    Enemy1(
                        random.randint(50, WIDTH - 50),
                        -50,
                        random.choice(enemy1_img),
                        diff_settings,
                    )
                )

            if (
                current_level_data["boss_type"]
                and score >= current_level_data["score_to_next_level"] - 1000
            ):
                if current_level_data["boss_type"] == Boss1 and not boss1_spawned:
                    boss1_group.add(Boss1(WIDTH // 2, -100, boss1_img, diff_settings))
                    boss1_spawned = True
                elif current_level_data["boss_type"] == Boss2 and not boss2_spawned:
                    boss2_group.add(Boss2(WIDTH // 2, -100, boss2_img, diff_settings))
                    boss2_spawned = True
                elif current_level_data["boss_type"] == Boss3 and not boss3_spawned:
                    boss3_group.add(Boss3(WIDTH // 2, -100, boss3_img, diff_settings))
                    boss3_spawned = True

            # Drawing
            for group in [
                enemy1_group,
                enemy2_group,
                boss1_group,
                boss2_group,
                boss3_group,
                bullets,
                enemy2_bullets,
                boss1_bullets,
                boss2_bullets,
                boss3_bullets,
                meteor_group,
                meteor2_group,
                black_hole_group,
                wormhole_group,
                bullet_refill_group,
                health_refill_group,
                extra_score_group,
                unlimited_bullet_refill_group,
                fire_rate_upgrade_group,
                explosions,
                explosions2,
            ]:
                group.draw(screen)

            screen.blit(player.image, player.rect)

            # UI
            screen.blit(life_bar_image, (10, 10))
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (45, 10, (player_life / diff_settings["player_life_start"]) * 150, 20),
            )
            screen.blit(bullet_bar_image, (10, 40))
            pygame.draw.rect(
                screen, (255, 255, 0), (45, 40, (min(bullet_counter, 200) / 200) * 150, 20)
            )

            # Boss Health Bars
            if boss1_spawned and boss1_health > 0:
                pygame.draw.rect(
                    screen, (255, 255, 255), (WIDTH // 2 - 100, 20, 200, 10), 2
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        WIDTH // 2 - 100,
                        20,
                        (boss1_health / (150 * diff_settings["boss_health_multiplier"]))
                        * 200,
                        10,
                    ),
                )
            elif boss2_spawned and boss2_health > 0:
                pygame.draw.rect(
                    screen, (255, 255, 255), (WIDTH // 2 - 100, 20, 200, 10), 2
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        WIDTH // 2 - 100,
                        20,
                        (boss2_health / (150 * diff_settings["boss_health_multiplier"]))
                        * 200,
                        10,
                    ),
                )
            elif boss3_spawned and boss3_health > 0:
                pygame.draw.rect(
                    screen, (255, 255, 255), (WIDTH // 2 - 100, 20, 200, 10), 2
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        WIDTH // 2 - 100,
                        20,
                        (boss3_health / (200 * diff_settings["boss_health_multiplier"]))
                        * 200,
                        10,
                    ),
                )

            score_txt = pygame.font.SysFont("Impact", 30).render(
                f"Score: {score}", True, (255, 255, 255)
            )
            screen.blit(score_txt, (WIDTH - 200, 10))

            if player_life <= 0:
                add_high_score("PLAYER", score)
                if show_game_over(screen, score) == "restart":
                    return "restart"
                return "menu"

            if score >= current_level_data["score_to_next_level"]:
                if current_level_idx < len(LEVELS) - 1:
                    current_level_idx += 1
                    current_level_data = LEVELS[current_level_idx]
                    current_bg_image = current_level_data["background_img"]
                    current_bg_top = current_level_data["background_img"].copy()
                    bg_y_shift = 0
                    pygame.mixer.Sound("game_sounds/warning.mp3").play()
                else:
                    add_high_score("PLAYER", score)
                    if show_game_win(screen) == "restart":
                        return "restart"
                    return "menu"

            pygame.display.flip()
            clock.tick(FPS)
    except Exception:
        logging.exception("Fatal error in run_game")
        return "menu"
    finally:
        logging.info("Exiting run_game")


if __name__ == "__main__":
    print("Please run 'menu.py' to start the game.")

