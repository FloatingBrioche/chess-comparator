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
    "Another Chess.com user",
    "A random grandmaster",
    "A random person from my country",
]

# Var used within request_helpers.get_puzzle

old_puzzle = {
    "url": "https://www.chess.com/daily-chess-puzzle/2024-10-25",
    "image": "https://www.chess.com/dynboard?fen=2n1k3/7N/8/1pPpB2p/3Pp1pP/P1q3P1/8/5RK1%20w%20-%20-%200%201&size=2",
}

required_game_archive_keys = {
    "initial_setup",
    "rated",
    "url",
    "tcn",
    "fen",
    "time_control",
    "rules",
    "white",
    "uuid",
    "pgn",
    "black",
    "time_class",
}

test_monthly_archives_small = [
    "https://api.chess.com/pub/player/aporian/games/2008/12",
    "https://api.chess.com/pub/player/aporian/games/2017/02",
    "https://api.chess.com/pub/player/aporian/games/2022/12",
    "https://api.chess.com/pub/player/aporian/games/2024/11",
    "https://api.chess.com/pub/player/aporian/games/2024/12",
]


test_monthly_archives_large = [
    "https://api.chess.com/pub/player/aporian/games/2008/12",
    "https://api.chess.com/pub/player/aporian/games/2009/03",
    "https://api.chess.com/pub/player/aporian/games/2009/04",
    "https://api.chess.com/pub/player/aporian/games/2009/05",
    "https://api.chess.com/pub/player/aporian/games/2009/06",
    "https://api.chess.com/pub/player/aporian/games/2009/07",
    "https://api.chess.com/pub/player/aporian/games/2009/08",
    "https://api.chess.com/pub/player/aporian/games/2009/09",
    "https://api.chess.com/pub/player/aporian/games/2009/12",
    "https://api.chess.com/pub/player/aporian/games/2010/01",
    "https://api.chess.com/pub/player/aporian/games/2010/05",
    "https://api.chess.com/pub/player/aporian/games/2010/06",
    "https://api.chess.com/pub/player/aporian/games/2011/10",
    "https://api.chess.com/pub/player/aporian/games/2011/11",
    "https://api.chess.com/pub/player/aporian/games/2011/12",
    "https://api.chess.com/pub/player/aporian/games/2012/05",
    "https://api.chess.com/pub/player/aporian/games/2012/06",
    "https://api.chess.com/pub/player/aporian/games/2012/07",
    "https://api.chess.com/pub/player/aporian/games/2012/08",
    "https://api.chess.com/pub/player/aporian/games/2012/09",
    "https://api.chess.com/pub/player/aporian/games/2012/10",
    "https://api.chess.com/pub/player/aporian/games/2012/11",
    "https://api.chess.com/pub/player/aporian/games/2012/12",
    "https://api.chess.com/pub/player/aporian/games/2013/01",
    "https://api.chess.com/pub/player/aporian/games/2013/02",
    "https://api.chess.com/pub/player/aporian/games/2013/03",
    "https://api.chess.com/pub/player/aporian/games/2013/04",
    "https://api.chess.com/pub/player/aporian/games/2013/05",
    "https://api.chess.com/pub/player/aporian/games/2013/06",
    "https://api.chess.com/pub/player/aporian/games/2013/07",
    "https://api.chess.com/pub/player/aporian/games/2013/08",
    "https://api.chess.com/pub/player/aporian/games/2013/09",
    "https://api.chess.com/pub/player/aporian/games/2013/11",
    "https://api.chess.com/pub/player/aporian/games/2014/01",
    "https://api.chess.com/pub/player/aporian/games/2014/02",
    "https://api.chess.com/pub/player/aporian/games/2014/06",
    "https://api.chess.com/pub/player/aporian/games/2014/07",
    "https://api.chess.com/pub/player/aporian/games/2014/08",
    "https://api.chess.com/pub/player/aporian/games/2014/11",
    "https://api.chess.com/pub/player/aporian/games/2014/12",
    "https://api.chess.com/pub/player/aporian/games/2015/01",
    "https://api.chess.com/pub/player/aporian/games/2015/03",
    "https://api.chess.com/pub/player/aporian/games/2016/02",
    "https://api.chess.com/pub/player/aporian/games/2016/03",
    "https://api.chess.com/pub/player/aporian/games/2016/04",
    "https://api.chess.com/pub/player/aporian/games/2016/05",
    "https://api.chess.com/pub/player/aporian/games/2016/07",
    "https://api.chess.com/pub/player/aporian/games/2016/09",
    "https://api.chess.com/pub/player/aporian/games/2016/11",
    "https://api.chess.com/pub/player/aporian/games/2017/01",
    "https://api.chess.com/pub/player/aporian/games/2017/02",
    "https://api.chess.com/pub/player/aporian/games/2017/04",
    "https://api.chess.com/pub/player/aporian/games/2017/11",
    "https://api.chess.com/pub/player/aporian/games/2020/01",
    "https://api.chess.com/pub/player/aporian/games/2020/02",
    "https://api.chess.com/pub/player/aporian/games/2020/03",
    "https://api.chess.com/pub/player/aporian/games/2020/04",
    "https://api.chess.com/pub/player/aporian/games/2020/05",
    "https://api.chess.com/pub/player/aporian/games/2020/06",
    "https://api.chess.com/pub/player/aporian/games/2020/07",
    "https://api.chess.com/pub/player/aporian/games/2020/08",
    "https://api.chess.com/pub/player/aporian/games/2020/09",
    "https://api.chess.com/pub/player/aporian/games/2020/10",
    "https://api.chess.com/pub/player/aporian/games/2020/11",
    "https://api.chess.com/pub/player/aporian/games/2020/12",
    "https://api.chess.com/pub/player/aporian/games/2021/01",
    "https://api.chess.com/pub/player/aporian/games/2022/07",
    "https://api.chess.com/pub/player/aporian/games/2022/11",
    "https://api.chess.com/pub/player/aporian/games/2022/12",
    "https://api.chess.com/pub/player/aporian/games/2024/09",
    "https://api.chess.com/pub/player/aporian/games/2024/10",
    "https://api.chess.com/pub/player/aporian/games/2024/11",
]
