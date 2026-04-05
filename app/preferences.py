import json
import os

PROFILE_PATH = "data/user_profiles.json"

def load_profiles():
    if not os.path.exists(PROFILE_PATH):
        return {}

    with open(PROFILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_profiles(profiles):
    with open(PROFILE_PATH, "w") as file:
        json.dump(profiles, file, indent=4)

def get_user_profile(username):
    profiles = load_profiles()
    return profiles.get(username, {"favorite_genres": [], "favorite_moods": [], "preferred_language": ""})

def update_user_profile(username, favorite_genres, favorite_moods, preferred_language):
    profiles = load_profiles()
    profiles[username] = {
        "favorite_genres": favorite_genres,
        "favorite_moods": favorite_moods,
        "preferred_language": preferred_language
    }
    save_profiles(profiles)