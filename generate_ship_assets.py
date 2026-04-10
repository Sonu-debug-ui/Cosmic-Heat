import pygame
import os


def generate_variations():
    pygame.init()
    # Need a display mode for convert_alpha to work
    pygame.display.set_mode((1, 1), pygame.HIDDEN)

    base_path = "images/omega_wing_base.png"

    if not os.path.exists(base_path):
        print(f"Error: {base_path} not found. Please place the ship image there.")
        return

    try:
        base_img = pygame.image.load(base_path).convert_alpha()
        print(f"Loaded {base_path} successfully.")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # 1. Crimson Ghost (Original Red)
    pygame.image.save(base_img, "images/crimson_ghost.png")
    print("Saved images/crimson_ghost.png")

    # 2. Neon Blade (Blue/Cyan Tint)
    neon_img = base_img.copy()
    blue_tint = pygame.Surface(neon_img.get_size(), pygame.SRCALPHA)
    blue_tint.fill((0, 100, 255, 120))  # Stronger Blue tint
    neon_img.blit(blue_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.image.save(neon_img, "images/neon_blade.png")
    print("Saved images/neon_blade.png")

    # 3. Omega Wing (Golden/Yellow Tint)
    omega_img = base_img.copy()
    gold_tint = pygame.Surface(omega_img.get_size(), pygame.SRCALPHA)
    gold_tint.fill((255, 215, 0, 130))  # Stronger Golden tint
    omega_img.blit(gold_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.image.save(omega_img, "images/omega_wing.png")
    print("Saved images/omega_wing.png")

    pygame.quit()


if __name__ == "__main__":
    generate_variations()
