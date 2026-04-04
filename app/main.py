import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="VibeBot🤖", page_icon="🎧", layout="centered")

st.title("VibeBot🤖🎧")
st.write("Your tunes for your mood 🎶")

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