import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="VibeBot🤖🎧")

st.title("VibeBot🤖🎧")
st.write("What mood are you in right now for some tunes 🎶")

user_input = st.text_input("How are you feeling")

if user_input:
    response = get_response(user_input)
    st.write("🤖 VibeBot: ", response)