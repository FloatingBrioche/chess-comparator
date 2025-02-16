import streamlit as st
import asyncio

from classes.chess_user import ChessUser
from classes.comparison import Comparison
from helpers.request_helpers import get_random_compatriot, get_random_gm, get_puzzle
from helpers.plot_helpers import plot_pie
from helpers.vars import indices, select_options


comparison_type = None
other = None
final_section = False

st.title(":chess_pawn: :rainbow[Chess.com Stats Comparator] :chess_pawn:")

st.write(
    "Welcome to the Chess.com Stats Comparator, an app that let's you compare your stats against those of other users through visualisations and tables."
)
st.text_input("Enter your Chess.com username to get started.", key="username")

username = st.session_state.username

if username:
    user = ChessUser(username)
    if user.profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        user.add_stats()
        st.divider()
        st.write(f"Welcome, {user.name}!")
        comparison_type = st.selectbox(
            "Who would like to compare yourself with?",
            select_options,
            index=None,
        )
        st.divider()

if comparison_type == "Myself":
    st.write("A wise choice. Comparison is the thief of joy, after all.")
    st.write("Here are your best ever ratings compared with your current ratings.")
    current_v_best_df = user.get_current_v_best()
    st.bar_chart(current_v_best_df, color=["#FF0000", "#0000FF"], stack=False)
    
    asyncio.run(user.get_game_history())
    user.wrangle_game_history_df()


if comparison_type == "Another Chess.com user":
    st.text_input("Please enter their Chess.com username", key="other_username")
    other_username = st.session_state.other_username
    if other_username:
        test = ChessUser(other_username)
        if test.profile is None:
            st.write("That username isn't right. Do you want to try another?")
        else:
            other = test

if comparison_type == "A random grandmaster":
    st.write("A bold choice. Let's see how you stack up against one of the greats.")
    other = ChessUser(get_random_gm())

if comparison_type == "A random person from my country":
    other = ChessUser(get_random_compatriot(user.country))

if other:
    other.add_stats()
    st.write(f"Alright, here's {user.name} vs. {other.name}!")
    comparison = Comparison(user, other)
    comparison.add_game_totals()
    actual_indices = comparison.df.index.to_list()

    u_col, oth_col = st.columns(2)

    with u_col:
        st.subheader(f"{user.name}")

        if "daily_wins" in actual_indices:
            u_daily_pie = plot_pie(comparison.df, user.username, indices["daily"])
            st.pyplot(u_daily_pie, clear_figure=True)

        if "rapid_wins" in actual_indices:
            u_rapid_pie = plot_pie(comparison.df, user.username, indices["rapid"])
            st.pyplot(u_rapid_pie, clear_figure=True)

        if "blitz_wins" in actual_indices:
            u_blitz_pie = plot_pie(comparison.df, user.username, indices["blitz"])
            st.pyplot(u_blitz_pie, clear_figure=True)

        if "bullet_wins" in actual_indices:
            u_bullet_pie = plot_pie(comparison.df, user.username, indices["bullet"])
            st.pyplot(u_bullet_pie, clear_figure=True)

        u_total_pie = plot_pie(comparison.df, user.username, indices["totals"])
        st.pyplot(u_total_pie, clear_figure=True)

    with oth_col:
        st.subheader(f"{other.name}")

        if "daily_wins" in actual_indices:
            oth_daily_pie = plot_pie(comparison.df, other.username, indices["daily"])
            st.pyplot(oth_daily_pie, clear_figure=True)

        if "rapid_wins" in actual_indices:
            oth_rapid_pie = plot_pie(comparison.df, other.username, indices["rapid"])
            st.pyplot(oth_rapid_pie, clear_figure=True)

        if "blitz_wins" in actual_indices:
            oth_blitz_pie = plot_pie(comparison.df, other.username, indices["blitz"])
            st.pyplot(oth_blitz_pie, clear_figure=True)

        if "bullet_wins" in actual_indices:
            oth_bullet_pie = plot_pie(comparison.df, other.username, indices["bullet"])
            st.pyplot(oth_bullet_pie, clear_figure=True)

        oth_total_pie = plot_pie(comparison.df, other.username, indices["totals"])
        st.pyplot(oth_total_pie, clear_figure=True)

    st.divider()

    comparison.add_avg_rating()

    st.bar_chart(comparison.df.filter(items=indices["ratings"], axis=0), stack=False)

    st.dataframe(comparison.get_head_to_head())
    st.caption(
        "(To see the full table, drag the bottom-right corner to expand it . . . . .    :point_up_2:)"
    )

    with st.expander("And the winner is..."):
        st.write(f"...{comparison.winner.name}!")
        st.markdown(
            f"""
                    | {user.name} | {other.name}|
                    |:---:|:---:|
                    | {user.total_points} points | {other.total_points} points |
                    """
        )
        if comparison.winner == user:
            st.write(f"Well, look at that, you formidable chess ninja!")
        if comparison.winner == other:
            st.write(
                f"Ah well, perhaps you need a little more practice. Here's a puzzle to start with."
            )
            puzzle: dict = get_puzzle()
            st.markdown(f"[![Chess puzzle]({puzzle["image"]})]({puzzle["url"]})")
        st.balloons()

    final_section = True

if final_section:

    st.divider()

    st.markdown(
        """
    ##### :balloon: :rainbow[Thanks for visiting!] :balloon:

    If you have any suggestions or comments about the app,  
    feel free to get in touch with me on [LinkedIn](https://www.linkedin.com/in/martincolbourne/) or check out the repo on my [GitHub](https://github.com/FloatingBrioche/).
    """
    )