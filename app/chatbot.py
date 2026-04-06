from recommender import recommend_songs
import pickle
import os
from spotify_client import search_tracks, search_playlists

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
        return "chill", 0.0, {}
    
    probabilities = mood_model.predict_proba([text])[0]
    labels = mood_model.named_steps["classifier"].classes_

    mood_scores = {
        label: float(prob)
        for label, prob in zip(labels, probabilities)
    }

    predicted_mood = max(mood_scores, key=mood_scores.get)
    confidence = mood_scores[predicted_mood]

    return predicted_mood, confidence, mood_scores

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

def build_spotify_query(mood, activity=None, favorite_genres=None):
    query_parts = [mood]

    if activity:
        query_parts.append(activity)

    if favorite_genres:
        query_parts.extend(favorite_genres[:2])

    return " ".join(query_parts)

def format_spotify_tracks(tracks):
    if not tracks:
        return "No Spotify tracks found."

    lines = []
    for track in tracks:
        lines.append(f"- [{track['name']} — {track['artist']}]({track['url']})")
    return "\n".join(lines)

def format_spotify_playlists(playlists):
    if not playlists:
        return "No Spotify playlists found."

    lines = []
    for playlist in playlists:
        lines.append(f"- [{playlist['name']}]({playlist['url']}) by *{playlist['owner']}*")
    return "\n".join(lines)

def get_response(user_input, favorite_genres=None, favorite_moods=None, preferred_language=None):
    mood, confidence, mood_scores = predict_mood(user_input)
    activity = detect_activity(user_input)
    songs = recommend_songs(
        mood,
        favorite_genres=favorite_genres,
        favorite_moods=favorite_moods,
        activity=activity,
        preferred_language=preferred_language
    )

    spotify_query = build_spotify_query(
        mood, activity=activity, favorite_genres=favorite_genres
    )

    spotify_tracks = search_tracks(spotify_query, limit=5)
    spotify_playlists = search_playlists(spotify_query, limit=3)

    intro_map = {
        "sad": "I’ve got some songs for your sad mood:",
        "happy": "Love that energy. Try these happy tracks:",
        "chill": "Here are some chill vibes for you:",
        "calm": "These should help you feel calm and relaxed:",
        "energetic": "Here are some energetic tracks to boost your mood:",
        "focused": "Try these songs to help you focus:"
    }

    if songs.empty:
        local_results = "I couldn't find songs for that mood yet 😅"
    else:
        local_results = format_song_results(songs)

    intro = intro_map.get(mood, "Here are some songs for you:")
    

    activity_text = f"**Detected activity:** `{activity}`\n\n" if activity else ""
    confidence_text = f"**Prediction confidence:** `{confidence:.2%}`\n\n"

    top_scores = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    score_lines = "\n".join([f"- `{label}`: {score:.2%}" for label, score in top_scores])
    score_text = f"**Top mood probabilities:**\n{score_lines}\n\n"

    spotify_tracks_text = format_spotify_tracks(spotify_tracks)
    spotify_playlists_text = format_spotify_playlists(spotify_playlists)

    return (
        f"**Predicted mood:** `{mood}`\n\n"
        f"{confidence_text}"
        f"{activity_text}"
        f"{score_text}"
        f"{intro}\n\n"
        f"### Local recommendations\n{local_results}\n\n"
        f"### Spotify tracks\n{spotify_tracks_text}\n\n"
        f"### Spotify playlists\n{spotify_playlists_text}"
    )