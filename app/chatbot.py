from recommender import recommend_songs


MOOD_KEYWORDS = {
    "sad": [
        "sad", "down", "upset", "heartbroken", "depressed", "cry", "low", "unhappy"
    ],
    "happy": [
        "happy", "good", "great", "excited", "joyful", "cheerful", "fun", "amazing"
    ],
    "chill": [
        "chill", "laid back", "easy", "vibing", "mellow"
    ],
    "calm": [
        "calm", "relaxed", "peaceful", "stress free", "meditation", "soothing", "stressed"
    ],
    "energetic": [
        "energetic", "gym", "workout", "exercise", "pump", "hype", "running", "party", "upbeat"
    ],
    "focused": [
        "focus", "focused", "study", "studying", "concentrate", "productivity", "work"
    ]
}

ACTIVITY_KEYWORDS = {
    "study": ["study", "studying", "focus", "homework", "revision"],
    "gym": ["gym", "workout", "exercise", "lifting", "training"],
    "sleep": ["sleep", "sleeping", "bed", "night", "rest"],
    "drive": ["drive", "driving", "road trip", "car"],
    "party": ["party", "dance", "club"],
    "relax": ["relax", "relaxing", "calm", "peaceful", "stress"],
    "work": ["work", "working", "coding", "office", "productive"]
}


def detect_mood(text):
    text = text.lower()
    mood_scores = {mood: 0 for mood in MOOD_KEYWORDS}

    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                mood_scores[mood] += 1

    best_mood = max(mood_scores, key=mood_scores.get)

    if mood_scores[best_mood] == 0:
        return "chill"

    return best_mood

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
    mood = detect_mood(user_input)
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

    return f"**Detected mood:** `{mood}`\n\n{activity_text}{intro}\n\n{results}"