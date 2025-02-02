# chess-comparator

A Streamlit app for Chess.com players that lets users visualise their chess stats and compare them with other players.

[![Tests](https://github.com/FloatingBrioche/chess-comparator/actions/workflows/tests.yaml/badge.svg)](https://github.com/FloatingBrioche/chess-comparator/actions/workflows/tests.yaml)
[![Coverage](./coverage.svg)][./coverage.txt]

## Languages/Libraries

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
- ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff)
- ![Matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff)
- ![httpx](https://img.shields.io/badge/httpx-v.0.28.1-blue)
- ![asyncio](https://img.shields.io/badge/asyncio-v.3.4.3-blue)

## Build Instructions

- To set up env and install requirements: `make requirements`
- To run pytest, black and coverage: `make run-checks`
- To run Streamlit app locally: `streamlit run main.py`

## Useful Links

- https://www.chess.com/news/view/published-data-api
- https://docs.streamlit.io/get-started