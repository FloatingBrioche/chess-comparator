import streamlit as st

from helpers.request_helpers import (
    get_profile,
    get_stats,
    get_random_gm,
    get_random_compatriot
)
from helpers.data_helpers import get_current_v_best, get_user_v_other, expand_data
from helpers.plot_helpers import plot_pie
from helpers.vars import blitz_indices, bullet_indices, daily_indices, rapid_indices, totals_indices, select_options, ratings_indices

st.title("Chess.com Stats Comparator")

st.text_input("Enter your Chess.com username", key="username")

username = st.session_state.username

user_profile: dict | None = get_profile(username)

comparison = None
other_username = None
st.divider()

if username:
    if user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        u_name = user_profile['name'] if user_profile.get('name') != None else username
        st.write(f"Welcome, {u_name}!")
        country = user_profile["country"].split("/")[-1]
        comparison = st.selectbox(
            "Who would like to compare yourself with?",
            select_options,
            index=None,
        )
        user_stats = get_stats(username)
        st.divider()

if comparison == "Myself":
    st.write("Alright then!")
    current_v_best_df = get_current_v_best(user_stats)
    st.line_chart(current_v_best_df, color=["#FF0000", "#0000FF"])

if comparison == "Another Chess.com user":
    st.text_input("Please enter their Chess.com username", key="other_username")
    other_username = st.session_state.other_username

if comparison == "A random grandmaster":
    other_username = get_random_gm()

if comparison == "A random person from my country":
    other_username = get_random_compatriot(country)

if other_username:
    other_user_profile: dict | None = get_profile(other_username)
    if other_user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        o_name = other_user_profile['name'] if other_user_profile.get('name') != None else other_username
        st.write(
            f"Alright, here's {u_name} vs. {o_name}!"
        )
        other_user_stats = get_stats(other_username)
        user_v_other_df = get_user_v_other(
            {username: user_stats},
            {other_username: other_user_stats},
        )
        user_v_other_df = expand_data(user_v_other_df)
        indices = user_v_other_df.index.to_list()
        u_col, oth_col = st.columns(2)

        with u_col:
            st.header(f"{u_name}")

            if "daily_wins" in indices:
                u_daily_pie = plot_pie(user_v_other_df, username, daily_indices)
                st.pyplot(u_daily_pie, clear_figure=True)

            if "rapid_wins" in indices:
                u_rapid_pie = plot_pie(user_v_other_df, username, rapid_indices)
                st.pyplot(u_rapid_pie, clear_figure=True)

            if "blitz_wins" in indices:
                u_blitz_pie = plot_pie(user_v_other_df, username, blitz_indices)
                st.pyplot(u_blitz_pie, clear_figure=True)

            if "bullet_wins" in indices:
                u_bullet_pie = plot_pie(user_v_other_df, username, bullet_indices)
                st.pyplot(u_bullet_pie, clear_figure=True)

            u_total_pie = plot_pie(user_v_other_df, username, totals_indices)
            st.pyplot(u_total_pie, clear_figure=True)

        with oth_col:
            st.header(f"{o_name}")

            if "daily_wins" in indices:
                oth_daily_pie = plot_pie(user_v_other_df, other_username, daily_indices)
                st.pyplot(oth_daily_pie, clear_figure=True)

            if "rapid_wins" in indices:
                oth_rapid_pie = plot_pie(user_v_other_df, other_username, rapid_indices)
                st.pyplot(oth_rapid_pie, clear_figure=True)

            if "blitz_wins" in indices:
                oth_blitz_pie = plot_pie(user_v_other_df, other_username, blitz_indices)
                st.pyplot(oth_blitz_pie, clear_figure=True)

            if "bullet_wins" in indices:
                oth_bullet_pie = plot_pie(
                    user_v_other_df, other_username, bullet_indices
                )
                st.pyplot(oth_bullet_pie, clear_figure=True)

            oth_total_pie = plot_pie(user_v_other_df, other_username, totals_indices)
            st.pyplot(oth_total_pie, clear_figure=True)

        st.divider()

        st.bar_chart(user_v_other_df.filter(items=ratings_indices, axis=0), stack=False)
        st.dataframe(user_v_other_df)

st.balloons()
