# chess-comparator
[![Tests](https://github.com/FloatingBrioche/chess-comparator/actions/workflows/tests.yaml/badge.svg)](https://github.com/FloatingBrioche/chess-comparator/actions/workflows/tests.yaml)
[![Coverage](./docs/coverage.svg)](./docs/coverage.txt)

A Streamlit app for Chess.com players that lets users visualise their chess stats and compare them with other players.

The app is built around the Chess.com API. Users' data is requested using the httpx library and then wrangled into a Pandas dataframe

<img src="./docs/chess_comparator_bar.png" width="60%" height="60%" alt="Example bar chart comparison">

<img src="./docs/chess_comparator_table.png" width="40%" height="40%" alt="Example table  comparison">

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

- [Chess.com API endpoints](https://www.chess.com/news/view/published-data-api)
- [Streamlit documentation](https://docs.streamlit.io/get-started)