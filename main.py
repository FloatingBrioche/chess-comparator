import streamlit as st
import requests
import polars as pl
import matplotlib.pyplot as plt

st.title("Chess.com Comparator")

st.text_input("Enter your Chess.com username", key="username")

username = st.session_state.username

user = requests.get(f'https://api.chess.com/pub/player/{username}/stats')