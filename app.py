import streamlit as st

from classes.chess_user import ChessUser
from classes.comparison import Comparison
from helpers.request_helpers import get_random_compatriot, get_random_gm, get_puzzle
from helpers.plot_helpers import plot_pie
from helpers.vars import indices, select_options

# placeholder vars for managing state
usage = None
comparison_type = None
other = None

st.set_page_config(
    page_title="Chess.com Stats Comparator",
    page_icon=":chess_pawn:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header(":chess_pawn: :rainbow[Chess.com Stats Comparator] :chess_pawn:")

with st.sidebar:
    st.write(
        "Welcome to the Chess.com Stats Comparator, an app that lets you explore and visualise your Chess.com stats and compare yourself with other players."
    )
    st.text_input("Enter your Chess.com username to get started.", key="username")

    if username := st.session_state.username:
        user = ChessUser(username)
        st.divider()
        if user.profile is None:
            st.write("That username isn't right. Do you want to try another?")
        else:
            user.add_stats()
            st.write(f"Hi, {user.name}!")
            usage = st.selectbox(
                "What would you like to do?",
                ["Check out my stats", "Compare stats"],
                index=None,
            )
            user.load_game_history()
            user_game_history_df = user.wrangle_game_history_df()
            user.add_accuracy_stats()
            match usage:
                case "Check out my stats":
                    st.write(
                        "A wise choice. Comparison is the thief of joy, after all."
                    )

    st.divider()

    st.markdown(
        """
    ##### :balloon: :rainbow[Thanks for visiting!] :balloon:

    If you have any suggestions or comments about the app,  
    feel free to check out the repo on [GitHub](https://github.com/FloatingBrioche/) 
    or get in touch on [LinkedIn](https://www.linkedin.com/in/martincolbourne/).
    """
    )


### Check out my stats
if usage == "Check out my stats":

    tab_openings, tab_opponents, tab_accuracy, tab_history = st.tabs(
        ["**Openings** :gift:", "**Opponents** :vs:", "**Accuracy** :mag:", "**History** :birthday:"]
    )
    
    def add_select_dim_options(section: str):
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            if include_colour := st.checkbox("Include colour?", value=False, key=f"{section}_colour"):
                dims.append("colour")
        with col_2:
            if include_time_class := st.checkbox("Include time class?", value=False, key=f"{section}_time_class"):
                dims.append("time_class")
        with col_3:
            if include_op_rating := st.checkbox("Include opponent rating?", value=False, key=f"{section}_op_rating"):
                dims.append("op_rating")
        
    with tab_openings:
        st.subheader(":rainbow[Openings]")
        openings_selection = None
        openings_selection = st.selectbox(
            "What would you like to see here?",
            [
                "My most played openings",
                "My most succesful openings",
                "My most accurate openings",
                "EVERYTHING!",
            ],
            index=None,
        )
        # opening counts
        if openings_selection == "My most played openings":
            dims = []
            add_select_dim_options("most_played_openings")
            opening_counts_df = user.query_game_history("url", ["eco", *dims])
            st.dataframe(opening_counts_df)
        # best openings by result
        elif openings_selection == "My most succesful openings":
            dims = []
            add_select_dim_options("most_succesful_openings")
            opening_results_df = (
                user.query_game_history("result", ["eco", *dims])
                .sort_values(by="win_pc", ascending=False)
                .head(10)
            )
            st.dataframe(opening_results_df)
        # best openings by accuracy
        elif openings_selection == "My most accurate openings":
            dims = []
            add_select_dim_options("most_accurate_openings")
            opening_accuracies_df = (
                user.query_game_history("accuracy", ["eco", *dims])
                .sort_values(by="accuracy", ascending=False)
                .head(10)
            )
            st.dataframe(opening_accuracies_df)
        # EVERYTHING!
        elif openings_selection == "EVERYTHING!":
            dims = []
            add_select_dim_options("everything")
            counts_df = user.query_game_history("url", ["eco", *dims])
            accuracies_df = user.query_game_history("accuracy", ["eco", *dims])
            success_df = user.query_game_history("result", ["eco", *dims])
            everything_df = counts_df.merge(
                accuracies_df, on=["eco", *dims], how="inner"
            ).merge(success_df, on=["eco", *dims], how="inner")
            st.dataframe(everything_df)

    with tab_opponents:
        st.subheader(":rainbow[Opponents]")
        opponents_selection = None
        opponents_selection = st.selectbox(
            "What would you like to see here?",
            [
                "My most played opponents",
                "My top-10 wins by rating differential",
                "My win percentages per opponent",
                "My accuracy per opponent",
            ],
            index=None,
        )
        # opponent counts
        if opponents_selection == "My most played opponents":
            dims = []
            opponent_counts_df = user.query_game_history("url", ["opponent", *dims]).head(10)
            st.bar_chart(opponent_counts_df, horizontal=True, x_label="Games played", color="#5D3FD3")
        # top-5 wins by rating differential
        if opponents_selection == "My top-10 wins by rating differential":
            top_10_by_rating = user.get_top_10("rating_differential", asc=True)
            st.dataframe(top_10_by_rating, hide_index=True)
        # results by opponent
        if opponents_selection == "My win percentages per opponent":
            dims = []
            add_select_dim_options("win_perc_per_opponent")
            wins_by_opp_df = user.query_game_history("result", ["opponent", *dims]).sort_values(by="opponent", ascending=True)
            st.dataframe(wins_by_opp_df)
        # accuracy by opponent
        if opponents_selection == "My accuracy per opponent":
            dims = []
            add_select_dim_options("accuracy_per_opponent")
            acc_by_opp_df = user.query_game_history("accuracy", ["opponent", *dims]).sort_values(by="opponent", ascending=True)
            st.dataframe(acc_by_opp_df)

    with tab_accuracy:
        st.subheader(":rainbow[Accuracy]")
        acc_selection = None
        acc_selection = st.selectbox(
            "What would you like to see here?",
            [
                "My most accurate wins",
                "My accuracy per opening",
                "My accuracy per opponent rating",
            ],
            index=None,
        )  # top-5 wins by accuracy games
        if acc_selection == "My most accurate wins":
            top_10_by_accuracy = user.get_top_10("accuracy")
            st.dataframe(top_10_by_accuracy, hide_index=True)
        # accuracy by opening
        if acc_selection == "My accuracy per opening":
            dims = []
            add_select_dim_options("accuracy_per_opening")
            acc_by_openings = user.query_game_history("accuracy", ["eco", *dims]).sort_values(by="eco", ascending=True)
            st.dataframe(acc_by_openings)
        # accuracy by op_rating
        if acc_selection == "My accuracy per opponent rating":
            dims = []
            acc_by_opp_rat = user.query_game_history("accuracy", ["op_rating", *dims])
            st.line_chart(acc_by_opp_rat, x_label="Opponent rating", y_label="Accuracy", color="#5D3FD3")

    with tab_history:
        st.subheader(":rainbow[History]")
        hist_selection = None
        hist_selection = st.selectbox(
            "What would you like to see here?",
            [
                "My current vs. best ratings",
                "My rating history",
                "My full game history",
            ],
            index=None,
        )
        # current vs. best ratings
        if hist_selection == "My current vs. best ratings":
            st.write(
                "Here are your best ever ratings compared with your current ratings."
            )
            current_v_best_df = user.get_current_v_best()
            st.bar_chart(current_v_best_df, color=["#FBDA00", "#5D3FD3"], stack=False, horizontal=True)
        # ratings history
        if hist_selection == "My rating history":
            time_selection = st.selectbox(
            "Which time class do you want to see?",
            [
                "Bullet",
                "Blitz",
                "Rapid",
                "Daily"
            ],
            index=None,
        )
            if time_selection: 
                rating_history_df = user.game_history_df[user.game_history_df['time_class'] == time_selection.lower()]['rating'].reset_index(drop=True)
                st.line_chart(rating_history_df)
                st.write("No te preocupes. Cada historia tiene sus altibajos.")
        # full game history
        if hist_selection == "My full game history":
            st.write(f"You've played {user.game_history_df.shape[0]} games. Here they are in all their glory!")
            st.dataframe(user_game_history_df)
            st.caption(
                "Click the column headers to sort or hide the columns, and see the other table options by hovering over the top-right of the table."
            )

### Compare stats

if usage == "Compare stats":
    comparison_type = st.selectbox(
        "Who would like to compare yourself with?",
        select_options,
        index=None,
    )

    if comparison_type == "Another Chess.com user":
        st.text_input("Please enter their Chess.com username", key="other_username")
        if other_username := st.session_state.other_username:
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
                oth_daily_pie = plot_pie(
                    comparison.df, other.username, indices["daily"]
                )
                st.pyplot(oth_daily_pie, clear_figure=True)

            if "rapid_wins" in actual_indices:
                oth_rapid_pie = plot_pie(
                    comparison.df, other.username, indices["rapid"]
                )
                st.pyplot(oth_rapid_pie, clear_figure=True)

            if "blitz_wins" in actual_indices:
                oth_blitz_pie = plot_pie(
                    comparison.df, other.username, indices["blitz"]
                )
                st.pyplot(oth_blitz_pie, clear_figure=True)

            if "bullet_wins" in actual_indices:
                oth_bullet_pie = plot_pie(
                    comparison.df, other.username, indices["bullet"]
                )
                st.pyplot(oth_bullet_pie, clear_figure=True)

            oth_total_pie = plot_pie(comparison.df, other.username, indices["totals"])
            st.pyplot(oth_total_pie, clear_figure=True)

        st.divider()

        comparison.add_avg_rating()

        st.bar_chart(
            comparison.df.filter(items=indices["ratings"], axis=0), stack=False, horizontal=True
        )

        st.dataframe(comparison.get_head_to_head())
        st.caption(
            "(To see the full table, drag the bottom-right corner to expand it . . . . .    :point_up_2:)"
        )
        st.divider()
        if st.button("Show me the winner!", icon=":material/trophy:"):
            st.write(f"The winner is... {comparison.winner.name}!")
            st.markdown(
                f"""
                        | {user.name} | {other.name}|
                        |:---:|:---:|
                        | {user.total_points} points | {other.total_points} points |
                        """
            )
            if comparison.winner == user:
                st.write("Well, look at that, you won!")
                st.balloons()
            if comparison.winner == other:
                st.write(
                    "Ah well, perhaps you need a little more practice. Here's a puzzle to start with."
                )
                puzzle: dict = get_puzzle()
                st.markdown(f"[![Chess puzzle]({puzzle["image"]})]({puzzle["url"]})")
            
