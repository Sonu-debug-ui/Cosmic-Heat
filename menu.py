import sys
import random
import logging
import traceback

# Set up logging to a file
logging.basicConfig(filename="game_debug.log", level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filemode='w') # Overwrite each time
logging.info("Game starting...")

try:
    import pygame
    import pygame.mixer
    pygame.init()
    pygame.font.init()
    logging.info("Pygame and Fonts initialized")
except Exception:
    logging.exception("Failed to initialize Pygame")
    sys.exit(1)

try:
    from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
    from high_score_manager import load_high_scores
    from settings_manager import save_settings, current_settings
    from classes.ship_config import SHIPS_CONFIG
    from functions import music_background
    import main
    logging.info("Imports from project modules successful")
except Exception:
    logging.exception("Failed to import project modules")
    sys.exit(1)

def show_hangar_menu():
    global current_settings
    logging.info("Entering Hangar Menu")
    running_hangar = True
    ship_names = list(SHIPS_CONFIG.keys())
    selected_ship_idx = 0
    title_font = pygame.font.SysFont("Impact", 60)
    name_font = pygame.font.SysFont("Comic Sans MS", 40)
    desc_font = pygame.font.SysFont("Comic Sans MS", 25)

    while running_hangar:
        ship_name = ship_names[selected_ship_idx]
        ship_info = SHIPS_CONFIG[ship_name]
        is_unlocked = ship_name in current_settings["unlocked_ships"]
        is_equipped = current_settings["equipped_ship"] == ship_name

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_hangar = False
                elif event.key == pygame.K_LEFT:
                    selected_ship_idx = (selected_ship_idx - 1) % len(ship_names)
                elif event.key == pygame.K_RIGHT:
                    selected_ship_idx = (selected_ship_idx + 1) % len(ship_names)
                elif event.key == pygame.K_RETURN:
                    if is_unlocked and not is_equipped:
                        current_settings["equipped_ship"] = ship_name
                        save_settings(current_settings)
                    elif not is_unlocked:
                        pass

        screen.fill(BLACK)
        title_text = title_font.render("HANGAR", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 80)))
        try:
            ship_img = pygame.image.load(ship_info["image_path"]).convert_alpha()
            ship_img = pygame.transform.scale(ship_img, (200, 200))
            if not is_unlocked:
                ship_img.fill((50, 50, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(ship_img, ship_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        except Exception:
            pygame.draw.rect(screen, RED, (WIDTH // 2 - 100, HEIGHT // 2 - 120, 200, 200), 2)

        name_color = WHITE if is_unlocked else (100, 100, 100)
        name_text = name_font.render(ship_name, True, name_color)
        screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120)))
        desc_text = desc_font.render(ship_info["description"], True, (200, 200, 200))
        screen.blit(desc_text, desc_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170)))
        status_str = ("EQUIPPED" if is_equipped else "SELECT (ENTER)" if is_unlocked else f"LOCKED ({current_settings['total_boss_kills']}/{ship_info['requirement']} Kills)")
        status_color = ((0, 255, 0) if is_equipped else (255, 255, 0) if is_unlocked else RED)
        status_text = name_font.render(status_str, True, status_color)
        screen.blit(status_text, status_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 230)))
        hint_text = desc_font.render("< Use Left / Right to Browse >", True, WHITE)
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
        pygame.display.flip()
        clock.tick(60)

def animate_screen():
    logging.info("Animating screen")
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)

def show_high_scores():
    logging.info("Showing High Scores")
    scores = load_high_scores()
    running_scores_screen = True
    while running_scores_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running_scores_screen = False

        screen.fill(BLACK)
        title_font = pygame.font.SysFont("Impact", 60)
        score_font = pygame.font.SysFont("Comic Sans MS", 30)
        title_text = title_font.render("HIGH SCORES", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 100)))
        y_offset = 200
        if scores:
            for i, entry in enumerate(scores):
                score_text = score_font.render(f"{i + 1}. {entry['name']}: {entry['score']}", True, WHITE)
                screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, y_offset + i * 40)))
        else:
            no_scores_text = score_font.render("No high scores yet!", True, WHITE)
            screen.blit(no_scores_text, no_scores_text.get_rect(center=(WIDTH // 2, y_offset)))
        return_text = score_font.render("Press ESC or ENTER to return", True, RED)
        screen.blit(return_text, return_text.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
        pygame.display.flip()
        clock.tick(60)

def show_settings_menu():
    global current_settings
    logging.info("Entering Settings Menu")
    settings = current_settings.copy()
    running_settings_screen = True
    selected_option = 0
    options_text = ["Music Volume:", "Sound Effects:", "Difficulty:", "Back"]
    difficulty_options = ["Easy", "Normal", "Hard"]

    while running_settings_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_settings_screen = False
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options_text)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options_text)
                elif event.key == pygame.K_LEFT:
                    if selected_option == 0:
                        settings["music_volume"] = max(0.0, settings["music_volume"] - 0.05)
                        pygame.mixer.music.set_volume(settings["music_volume"])
                    elif selected_option == 1:
                        settings["sound_effects"] = max(0.0, settings["sound_effects"] - 0.05)
                    elif selected_option == 2:
                        current_idx = difficulty_options.index(settings["difficulty"])
                        settings["difficulty"] = difficulty_options[(current_idx - 1) % len(difficulty_options)]
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 0:
                        settings["music_volume"] = min(1.0, settings["music_volume"] + 0.05)
                        pygame.mixer.music.set_volume(settings["music_volume"])
                    elif selected_option == 1:
                        settings["sound_effects"] = min(1.0, settings["sound_effects"] + 0.05)
                    elif selected_option == 2:
                        current_idx = difficulty_options.index(settings["difficulty"])
                        settings["difficulty"] = difficulty_options[(current_idx + 1) % len(difficulty_options)]
                elif event.key == pygame.K_RETURN:
                    if selected_option == len(options_text) - 1:
                        current_settings = settings.copy()
                        save_settings(current_settings)
                        running_settings_screen = False

        screen.fill(BLACK)
        title_font = pygame.font.SysFont("Impact", 60)
        option_font = pygame.font.SysFont("Comic Sans MS", 35)
        title_text = title_font.render("SETTINGS", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 100)))
        y_offset = 200
        for i, option_text in enumerate(options_text):
            color = RED if i == selected_option else WHITE
            val = ""
            if i == 0: val = f"{int(settings['music_volume'] * 100)}%"
            elif i == 1: val = f"{int(settings['sound_effects'] * 100)}%"
            elif i == 2: val = settings['difficulty']
            rendered = option_font.render(f"{option_text} {val}", True, color)
            screen.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y_offset + i * 50)))
        pygame.display.flip()
        clock.tick(60)

try:
    logging.info("Initializing Mixer and Display")
    pygame.mixer.init()
    pygame.mixer.music.load("game_sounds/menu.mp3")
    pygame.mixer.music.set_volume(current_settings["music_volume"])
    pygame.mixer.music.play(-1)
    pygame.mixer.set_num_channels(20)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    logging.info("Window created successfully")

    mainmenu_img = pygame.image.load("images/mainmenu.png").convert()
    mainmenu_img = pygame.transform.smoothscale(mainmenu_img, (WIDTH, HEIGHT))
    logo_img = pygame.image.load("images/ch.png").convert_alpha()
    logo_width = 350
    logo_height = int(logo_width * (logo_img.get_height() / logo_img.get_width()))
    logo_img = pygame.transform.smoothscale(logo_img, (logo_width, logo_height))
    logo_x, logo_y = (WIDTH - logo_width) // 2, 20

    play_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 50)
    hangar_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 45, 300, 50)
    high_scores_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 110, 300, 50)
    settings_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 175, 300, 50)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 240, 300, 50)

    explosion_sound = pygame.mixer.Sound("game_sounds/explosions/explosion1.wav")
    explosion_sound.set_volume(0.25)
    selected_button = 0
    show_menu = True
    logging.info("Assets loaded successfully")

    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        logging.info("Joystick initialized")

    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event received")
                show_menu = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    explosion_sound.play()
                    animate_screen()
                    game_result = "restart"
                    while game_result == "restart":
                        game_result = main.run_game(screen)
                    logging.info(f"Game session ended with result: {game_result}")
                    if game_result == "quit":
                        show_menu = False
                    elif game_result == "menu":
                        pygame.mixer.music.load("game_sounds/menu.mp3")
                        pygame.mixer.music.set_volume(current_settings["music_volume"])
                        pygame.mixer.music.play(-1)
                    break
                elif hangar_button_rect.collidepoint(event.pos): show_hangar_menu()
                elif high_scores_button_rect.collidepoint(event.pos): show_high_scores()
                elif settings_button_rect.collidepoint(event.pos):
                    show_settings_menu()
                    pygame.mixer.music.set_volume(current_settings["music_volume"])
                elif quit_button_rect.collidepoint(event.pos): show_menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_button = (selected_button - 1) % 5
                elif event.key == pygame.K_DOWN: selected_button = (selected_button + 1) % 5
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen()
                        game_result = "restart"
                        while game_result == "restart":
                            game_result = main.run_game(screen)
                        logging.info(f"Game session ended with result: {game_result}")
                        if game_result == "quit":
                            show_menu = False
                        elif game_result == "menu":
                            pygame.mixer.music.load("game_sounds/menu.mp3")
                            pygame.mixer.music.set_volume(current_settings["music_volume"])
                            pygame.mixer.music.play(-1)
                        break
                    elif selected_button == 1: show_hangar_menu()
                    elif selected_button == 2: show_high_scores()
                    elif selected_button == 3:
                        show_settings_menu()
                        pygame.mixer.music.set_volume(current_settings["music_volume"])
                    elif selected_button == 4: show_menu = False

            if joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_button == 0:
                            explosion_sound.play()
                            animate_screen()
                            game_result = "restart"
                            while game_result == "restart":
                                game_result = main.run_game(screen)
                            logging.info(f"Game session ended with result: {game_result}")
                            if game_result == "quit":
                                show_menu = False
                            elif game_result == "menu":
                                pygame.mixer.music.load("game_sounds/menu.mp3")
                                pygame.mixer.music.set_volume(current_settings["music_volume"])
                                pygame.mixer.music.play(-1)
                            break
                        elif selected_button == 1: show_hangar_menu()
                        elif selected_button == 2: show_high_scores()
                        elif selected_button == 3:
                            show_settings_menu()
                            pygame.mixer.music.set_volume(current_settings["music_volume"])
                        elif selected_button == 4: show_menu = False
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[1] == 1: selected_button = (selected_button - 1) % 5
                    elif event.value[1] == -1: selected_button = (selected_button + 1) % 5

        screen.blit(mainmenu_img, (0, 0))
        screen.blit(logo_img, (logo_x, logo_y))
        font = pygame.font.SysFont("Comic Sans MS", 40)
        for i, (rect, label) in enumerate([(play_button_rect, "Play"), (hangar_button_rect, "Hangar"), (high_scores_button_rect, "High Scores"), (settings_button_rect, "Settings"), (quit_button_rect, "Exit")]):
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)
            if selected_button == i: pygame.draw.rect(screen, RED, rect, border_radius=10, width=4)
            txt = font.render(label, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))
        pygame.display.flip()
        clock.tick(60)

except Exception:
    logging.exception("Fatal error in main menu")
finally:
    logging.info("Game exiting...")
    pygame.quit()
    sys.exit()
