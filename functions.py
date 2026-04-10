import pygame
import sys
from classes.constants import WIDTH, HEIGHT

def music_background():
    pygame.mixer.music.load("game_sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(loops=-1)


def draw_interactive_menu(screen, title_text, title_color, score=None):
    font = pygame.font.SysFont("Impact", 60)
    font_small = pygame.font.SysFont("Impact", 35)

    options = ["RESTART", "HOME"]
    selected_option = 0

    clock = pygame.time.Clock()

    while True:
        # Drawing
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Title
        title_render = font.render(title_text, True, title_color)
        title_rect = title_render.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_render, title_rect)

        # Score (if provided)
        if score is not None:
            score_render = font_small.render(
                f"Final Score: {score}", True, (255, 255, 255)
            )
            score_rect = score_render.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
            screen.blit(score_render, score_rect)

        # Buttons
        button_rects = []
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            text_render = font_small.render(option, True, color)
            text_rect = text_render.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 20 + i * 80)
            )

            # Simple button background
            bg_rect = pygame.Rect(0, 0, 250, 60)
            bg_rect.center = text_rect.center
            button_rects.append(bg_rect)

            pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=10)
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), bg_rect, 3, border_radius=10)

            screen.blit(text_render, text_rect)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return "restart" if selected_option == 0 else "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        return "restart" if i == 0 else "menu"

        clock.tick(60)


def show_game_over(screen, score):
    pygame.mixer.music.load("game_sounds/gameover.mp3")
    pygame.mixer.music.play(-1)

    result = draw_interactive_menu(screen, "GAME OVER", (139, 0, 0), score)

    music_background()
    return result


def show_game_win(screen):
    pygame.mixer.music.load("game_sounds/win.mp3")
    pygame.mixer.music.play()

    result = draw_interactive_menu(screen, "AWESOME! YOU WIN!", (0, 200, 0))

    music_background()
    return result
