import pandas as pd


def get_current_v_best(user_stats):
    stats = {"current": {}, "best": {}}
    for k, v in user_stats.items():
        if "last" in v:
            if "rating" in v["last"]:
                stats["current"][k.removeprefix('chess_')] = v["last"]["rating"]
        if "best" in v:
            if "rating" in v["best"]:
                stats["best"][k.removeprefix('chess_')] = v["best"]["rating"]
    return pd.DataFrame.from_dict(stats, orient="columns")

