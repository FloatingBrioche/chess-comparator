import streamlit as st
import matplotlib.pyplot as plt
from helpers import get_stats

st.title("Chess.com Comparator")

st.text_input("Enter your Chess.com username", key="username")

username = st.session_state.username

user_stats: dict | None = get_stats(username)
