import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "music_volume": 0.25,
    "sound_effects": 0.4,
    "difficulty": "Normal",  # Could be "Easy", "Normal", "Hard"
    "total_boss_kills": 0,
    "unlocked_ships": ["Standard"],
    "equipped_ship": "Standard",
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            # Merge with default settings to ensure all keys exist
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
            return settings
    except json.JSONDecodeError:
        print(f"Warning: {SETTINGS_FILE} is corrupt. Using default settings.")
        return DEFAULT_SETTINGS.copy()
    except Exception as e:
        print(f"Error loading settings: {e}. Using default settings.")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")


# This will be used in main.py and menu.py
current_settings = load_settings()
