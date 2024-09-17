import streamlit as st
from request_helpers import get_profile, get_stats
from data_helpers import get_current_v_best, get_user_v_other

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
            index=None,
        )
        user_stats = get_stats(username)
        st.divider()

if comparison == "My best self":
    st.write("Alright then!")
    current_v_best_df = get_current_v_best(user_stats)
    cols = current_v_best_df.columns.to_list()
    st.line_chart(current_v_best_df, color=["#FF0000", "#0000FF"])

if comparison == "Another Chess.com user":
    st.text_input("Please enter their Chess.com username", key="other_username")
    other_username = st.session_state.other_username
    other_user_profile: dict | None = get_profile(other_username)
    if other_user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        st.write(
            f"Alright, let's take a look at {user_profile['name']} vs. {other_user_profile['name']}!"
        )
        other_user_stats = get_stats(other_username)
        get_user_v_other(
            {f"{user_profile['name']}": user_stats},
            {f"{other_user_profile['name']}": other_user_stats}
        )
