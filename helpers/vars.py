# Vars used within main.py

indices = {
    "blitz": ["blitz_wins", "blitz_draws", "blitz_losses"],
    "bullet": ["bullet_wins", "bullet_draws", "bullet_losses"],
    "daily": ["daily_wins", "daily_draws", "daily_losses"],
    "rapid": ["rapid_wins", "rapid_draws", "rapid_losses"],
    "totals": ["total_wins", "total_draws", "total_losses"],
    "ratings": [
        "daily_best",
        "daily_current",
        "rapid_best",
        "rapid_current",
        "blitz_best",
        "blitz_current",
        "bullet_best",
        "bullet_current",
        "FIDE",
        "puzzles",
        "avg_rating_current",
    ],
}

select_options = [
    "Myself",
    "Another Chess.com user",
    "A random grandmaster",
    "A random person from my country",
]

# Var used within request_helpers.get_puzzle

old_puzzle = {
    "url": "https://www.chess.com/daily-chess-puzzle/2024-10-25",
    "image": "https://www.chess.com/dynboard?fen=2n1k3/7N/8/1pPpB2p/3Pp1pP/P1q3P1/8/5RK1%20w%20-%20-%200%201&size=2",
}

archive_keys = {'initial_setup', 'rated', 'url', 'tcn', 'fen', 'time_control', 'rules', 'white', 'eco', 'end_time', 'uuid', 'start_time', 'pgn', 'black', 'time_class'}