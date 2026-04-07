import streamlit as st
from chatbot import get_response
from preferences import get_user_profile, update_user_profile

st.set_page_config(page_title="VibeBot 🎧", page_icon="🎧", layout="centered")

st.title("🎧 VibeBot")
st.caption("Your mood-based music chatbot")

with st.sidebar:
    st.header("Your Profile")

    developer_mode = st.checkbox("Developer mode", value = False)

    username = st.text_input("Enter your username", value="guest")

    all_genres = ["pop", "rock", "hip-hop", "ambient", "chill", "alternative", "edm", "indie", "instrumental", "classical", "lofi"]
    all_moods = ["sad", "happy", "chill", "calm", "energetic", "focused"]
    all_languages = ["", "english", "instrumental"]

    profile = get_user_profile(username)

    favorite_genres = st.multiselect(
        "Favorite genres",
        all_genres,
        default=profile.get("favorite_genres", [])
    )

    favorite_moods = st.multiselect(
        "Favorite moods",
        all_moods,
        default=profile.get("favorite_moods", [])
    )

    preferred_language = st.selectbox(
        "Preferred language",
        all_languages,
        index=all_languages.index(profile.get("preferred_language", "")) if profile.get("preferred_language", "") in all_languages else 0
    )

    if st.button("Save Preferences"):
        update_user_profile(username, favorite_genres, favorite_moods, preferred_language)
        st.success("Preferences saved!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! I'm VibeBot 🎧\nTell me your mood, activity, or vibe, I'll find the perfect music for you."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("How are you feeling right now?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(user_input, favorite_genres=favorite_genres, favorite_moods=favorite_moods, preferred_language=preferred_language, developer_mode=developer_mode)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)