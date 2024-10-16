import streamlit as st

from helpers.request_helpers import (
    get_profile,
    get_stats,
    get_random_gm,
    get_random_compatriot
)
from helpers.data_helpers import (
    get_current_v_best,
    get_user_v_other,
    expand_data,
    get_head_to_head
)
from helpers.plot_helpers import plot_pie
from helpers.vars import indices, select_options

comparison = None
other_username = None

st.title(":chess_pawn: :rainbow[Chess.com Stats Comparator] :chess_pawn:")

st.write("Welcome to the Chess.com Stats Comparator, an app that let's you compare your stats against those of other users through visualisations and tables.")
st.text_input("Enter your Chess.com username to get started.", key="username")

username = st.session_state.username

user_profile: dict | None = get_profile(username)


st.divider()

if username:
    if user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        u_name = (
            user_profile["name"] if user_profile.get("name") is not None else username
        )
        st.write(f"Welcome, {u_name}!")
        country = user_profile["country"].split("/")[-1]
        comparison = st.selectbox(
            "Who would like to compare yourself with?",
            select_options,
            index=None,
        )
        user_stats: dict = get_stats(username)
        st.divider()

if comparison == "Myself":
    st.write("A wise choice. Comparison is the thief of joy, after all.")
    st.write("Here are your best ever ratings compared with your current ratings.")
    current_v_best_df = get_current_v_best(user_stats)
    st.bar_chart(current_v_best_df, color=["#FF0000", "#0000FF"], stack=False)

if comparison == "Another Chess.com user":
    st.text_input("Please enter their Chess.com username", key="other_username")
    other_username = st.session_state.other_username

if comparison == "A random grandmaster":
    st.write("A bold choice. Let's see how you stack up against one of the greats.")
    other_username = get_random_gm()

if comparison == "A random person from my country":
    other_username = get_random_compatriot(country)

if other_username:
    other_user_profile: dict | None = get_profile(other_username)
    if other_user_profile is None:
        st.write("That username isn't right. Do you want to try another?")
    else:
        o_name = (
            other_user_profile["name"]
            if other_user_profile.get("name") is not None
            else other_username
        )
        st.write(f"Alright, here's {u_name} vs. {o_name}!")
        other_user_stats = get_stats(other_username)
        user_v_other_df = get_user_v_other(
            {username: user_stats},
            {other_username: other_user_stats},
        )
        user_v_other_df = expand_data(user_v_other_df)
        actual_indices = user_v_other_df.index.to_list()
        u_col, oth_col = st.columns(2)

        with u_col:
            st.subheader(f"{u_name}")

            if "daily_wins" in actual_indices:
                u_daily_pie = plot_pie(user_v_other_df, username, indices["daily"])
                st.pyplot(u_daily_pie, clear_figure=True)

            if "rapid_wins" in actual_indices:
                u_rapid_pie = plot_pie(user_v_other_df, username, indices["rapid"])
                st.pyplot(u_rapid_pie, clear_figure=True)

            if "blitz_wins" in actual_indices:
                u_blitz_pie = plot_pie(user_v_other_df, username, indices["blitz"])
                st.pyplot(u_blitz_pie, clear_figure=True)

            if "bullet_wins" in actual_indices:
                u_bullet_pie = plot_pie(user_v_other_df, username, indices["bullet"])
                st.pyplot(u_bullet_pie, clear_figure=True)

            u_total_pie = plot_pie(user_v_other_df, username, indices["totals"])
            st.pyplot(u_total_pie, clear_figure=True)

        with oth_col:
            st.subheader(f"{o_name}")

            if "daily_wins" in actual_indices:
                oth_daily_pie = plot_pie(
                    user_v_other_df, other_username, indices["daily"]
                )
                st.pyplot(oth_daily_pie, clear_figure=True)

            if "rapid_wins" in actual_indices:
                oth_rapid_pie = plot_pie(
                    user_v_other_df, other_username, indices["rapid"]
                )
                st.pyplot(oth_rapid_pie, clear_figure=True)

            if "blitz_wins" in actual_indices:
                oth_blitz_pie = plot_pie(
                    user_v_other_df, other_username, indices["blitz"]
                )
                st.pyplot(oth_blitz_pie, clear_figure=True)

            if "bullet_wins" in actual_indices:
                oth_bullet_pie = plot_pie(
                    user_v_other_df, other_username, indices["bullet"]
                )
                st.pyplot(oth_bullet_pie, clear_figure=True)

            oth_total_pie = plot_pie(user_v_other_df, other_username, indices["totals"])
            st.pyplot(oth_total_pie, clear_figure=True)

        st.divider()

        st.bar_chart(
            user_v_other_df.filter(items=indices["ratings"], axis=0), stack=False
        )
        

        st.dataframe(get_head_to_head(user_v_other_df))



st.divider()

# if u_wins:

#     st.balloons()
#     st.divider()
# elif o_wins:
#     st.snow()
#     st.divider()



st.markdown(
    '''
    ##### :balloon: :rainbow[Thanks for visiting!] :balloon:

    If you have any suggestions or comments about the app,  
    feel free to get in touch with me on [LinkedIn](https://www.linkedin.com/in/martincolbourne/) or check out the repo on my [GitHub](https://github.com/FloatingBrioche/).
    '''
    )

