import json
import os

SETTINGS_FILE = "game_settings.json"

DEFAULT_SETTINGS = {
    "fullscreen": True
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


def get_fullscreen():
    settings = load_settings()
    return settings.get("fullscreen", True)


def set_fullscreen(value):
    settings = load_settings()
    settings["fullscreen"] = value
    save_settings(settings)