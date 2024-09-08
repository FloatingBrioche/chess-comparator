import streamlit as st
import matplotlib.pyplot as plt
from request_helpers import get_profile, get_stats
from data_helpers import get_current_self, get_best_self

st.title("Chess.com Comparator")

st.text_input("Enter your Chess.com username", key="username")

username = st.session_state.username

user_profile: dict | None = get_profile(username)

comparison = None

st.divider()

if username:
    if user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        st.write(f"Welcome, {user_profile['name']}!")
        comparison = st.selectbox(
            "Who would like to compare yourself with?",
            [
                "My best self",
                "Another Chess.com user",
                "A random grandmaster",
                "A random person from my country",
            ],
            index=None
        )
        user_stats = get_stats(username)
        st.divider()

if comparison == "My best self":
    st.write("Alright then!")
    current_self = get_current_self(user_stats)
    best_self = get_best_self(user_stats)