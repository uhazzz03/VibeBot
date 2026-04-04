from recommender import recommend_songs

MOOD_KEYWORDS = {
    "sad": [
        "sad", "down", "upset", "heartbroken", "depressed", "cry", "low", "unhappy"
    ],
    "happy": [
        "happy", "good", "great", "excited", "joyful", "cheerful", "fun"
    ],
    "chill": [
        "chill", "laid back", "easy", "vibing", "mellow"
    ],
    "calm": [
        "calm", "relaxed", "peaceful", "stress free", "meditation", "soothing"
    ],
    "energetic": [
        "energetic", "gym", "workout", "exercise", "pump", "hype", "running", "party", "upbeat"
    ],
    "focused": [
        "focus", "focused", "study", "studying", "concentrate", "productivity", "work"
    ]
}

def detect_mood(text):
    text = text.lower()

    mood_scores = {mood: 0 for mood in MOOD_KEYWORDS}

    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                mood_scores[mood] += 1
    
    best_mood = max(mood_scores, key = mood_scores.get)

    if mood_scores[best_mood] == 0:
        return "chill"
    
    return best_mood
    
def format_song_results(songs):
    lines = []
    for _, row in songs.iterrows():
        lines.append(f"- **{row['song']}** by *{row['artist']}*  \n  Genre: `{row['genre']}`")
    return "\n\n".join(lines)


def get_response(user_input):
    mood = detect_mood(user_input)
    songs = recommend_songs(mood)

    intro_map = {
        "sad": "I’ve got some songs for your sad mood:",
        "happy": "Love that energy. Try these happy tracks:",
        "chill": "Here are some chill vibes for you:",
        "calm": "These should help you feel calm and relaxed:",
        "energetic": "Here are some energetic tracks to boost your mood:",
        "focused": "Try these songs to help you focus:"
    }

    if songs.empty:
        return "I couldn't find songs for that mood 😅"


    intro = intro_map.get(mood, "Here are some songs for you:")
    results = format_song_results(songs)

    return f"**Detected mood:** `{mood}`\n\n{intro}\n\n{results}"