import streamlit as st
from chatbot import get_response
from preferences import get_user_profile, update_user_profile

st.set_page_config(page_title="VibeBot🤖", page_icon="🎧", layout="centered")

st.title("VibeBot🤖🎧")
st.write("Your tunes for your mood 🎶")

with st.sidebar:
    st.header("Your Profile")

    username = st.text_input("Enter your username", value="guest")

    all_genres = ["pop", "rock", "hip-hop", "ambient", "chill", "alternative", "edm", "indie", "instrumental", "classical", "lofi"]
    all_moods = ["sad", "happy", "chill", "calm", "energetic", "focused"]

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

    if st.button("Save Preferences"):
        update_user_profile(username, favorite_genres, favorite_moods)
        st.success("Preferences saved!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "What mood are you in right now for some tunes, let me know :)"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("How are you feeling now?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)