from recommender import recommend_songs

def detect_mood(text):
    text = text.lower()

    if "sad" in text:
        return "sad"
    elif "happy" in text:
        return "happy"
    elif "chill" in text:
        return "chill"
    elif "calm" in text:
        return "calm"
    elif "gym" in text or "workout" in text:
        return "energetic"
    else:
        return "energetic"
    
def get_response(user_input):
    mood = detect_mood(user_input)
    songs = recommend_songs(mood)

    if songs.empty:
        return "I couldn't find songs for that mood 😅"

    response = f"Here are some {mood} songs:\n"

    for _, row in songs.iterrows():
        response += f"- {row['song']} by {row['artist']}\n"

    return response