from recommender import recommend_songs
import pickle
import os

MODEL_PATH = "models/mood_classifier.pkl"

mood_model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as file:
        mood_model = pickle.load(file)

ACTIVITY_KEYWORDS = {
    "study": ["study", "studying", "focus", "homework", "revision"],
    "gym": ["gym", "workout", "exercise", "lifting", "training"],
    "sleep": ["sleep", "sleeping", "bed", "night", "rest"],
    "drive": ["drive", "driving", "road trip", "car"],
    "party": ["party", "dance", "club"],
    "relax": ["relax", "relaxing", "calm", "peaceful", "stress"],
    "work": ["work", "working", "coding", "office", "productive"]
}


def predict_mood(text):
    if mood_model is None:
        return "chill"
    return mood_model.predict([text])[0]

def detect_activity(text):
    text = text.lower()
    activity_scores = {activity: 0 for activity in ACTIVITY_KEYWORDS}

    for activity, keywords in ACTIVITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                activity_scores[activity] += 1

    best_activity = max(activity_scores, key=activity_scores.get)

    if activity_scores[best_activity] == 0:
        return None

    return best_activity

def format_song_results(songs):
    lines = []
    for _, row in songs.iterrows():
        lines.append(
            f"- **{row['song']}** by *{row['artist']}*  \n"
            f"  Genre: `{row['genre']}` | Mood: `{row['mood']}` | Activity: `{row['activity']}` | Score: `{round(row['score'], 2)}`"
        )
    return "\n\n".join(lines)


def get_response(user_input, favorite_genres=None, favorite_moods=None, preferred_language=None):
    mood = predict_mood(user_input)
    activity = detect_activity(user_input)
    songs = recommend_songs(
        mood,
        favorite_genres=favorite_genres,
        favorite_moods=favorite_moods,
        activity=activity,
        preferred_language=preferred_language
    )

    intro_map = {
        "sad": "I’ve got some songs for your sad mood:",
        "happy": "Love that energy. Try these happy tracks:",
        "chill": "Here are some chill vibes for you:",
        "calm": "These should help you feel calm and relaxed:",
        "energetic": "Here are some energetic tracks to boost your mood:",
        "focused": "Try these songs to help you focus:"
    }

    if songs.empty:
        return "I couldn't find songs for that mood yet 😅"

    intro = intro_map.get(mood, "Here are some songs for you:")
    results = format_song_results(songs)

    activity_text = f"**Detected activity:** `{activity}`\n\n" if activity else ""

    return f"**Predicted mood:** `{mood}`\n\n{activity_text}{intro}\n\n{results}"