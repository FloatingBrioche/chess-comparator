import streamlit as st
import matplotlib.pyplot as plt
from helpers.vars import vars
from helpers.request_helpers import get_profile, get_stats
from helpers.data_helpers import get_current_v_best, get_user_v_other, expand_data
from helpers.plot_helpers import plot_pie

st.title("Chess.com Stats Comparator")

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
            vars['select_options'],
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
            f"Alright, here's {user_profile['name']} vs. {other_user_profile['name']}!"
        )
        other_user_stats = get_stats(other_username)
        user_v_other_df = get_user_v_other(
            {username: user_stats},
            {other_username: other_user_stats},
        )
        user_v_other_df = expand_data(user_v_other_df)

        st.dataframe(user_v_other_df)
        
        u_col, oth_col = st.columns(2)

        with u_col:
            st.header(f"{user_profile['name']}")

            u_pie = plot_pie(user_v_other_df, username, vars["totals"])
            st.pyplot(u_pie.figure)


        with oth_col:
            st.header(f"{other_user_profile['name']}")

            oth_pie = plot_pie(user_v_other_df, other_username, vars["totals"])
            st.pyplot(oth_pie.figure)

st.balloons()
