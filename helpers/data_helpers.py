import pandas as pd


def get_current_v_best(u_stats) -> pd.DataFrame:
    stats = {"current": {}, "best": {}}
    for k, v in u_stats.items():
        if "last" in v:
            if "rating" in v["last"]:
                stats["current"][k.removeprefix('chess_')] = v["last"]["rating"]
        if "best" in v:
            if "rating" in v["best"]:
                stats["best"][k.removeprefix('chess_')] = v["best"]["rating"]
    return pd.DataFrame.from_dict(stats, orient="columns")


def get_user_v_other(user: dict, other: dict) -> pd.DataFrame:
    user_name, other_name = list(user.keys())[0], list(other.keys())[0]
    u_stats, oth_stats = user[user_name], other[other_name]
    stats = {user_name: {}, other_name: {}}
    u, oth = stats[user_name], stats[other_name]
    available_user_metrics = set(u_stats.keys())
    available_other_metrics = set(oth_stats.keys())
    comparable_metrics = available_user_metrics.intersection(available_other_metrics)
    
    for metric in comparable_metrics:
        metric_name = metric.removeprefix('chess_')
        if "record" in u_stats[metric]:
            u[metric_name + "_best"] = u_stats[metric]["best"]["rating"]
            u[metric_name + "_current"] = u_stats[metric]["last"]["rating"]
            u[metric_name + "_wins"] = u_stats[metric]["record"]["win"]
            u[metric_name + "_draws"] = u_stats[metric]["record"]["draw"]            
            u[metric_name + "_losses"] = u_stats[metric]["record"]["loss"]
            
            oth[metric_name + "_best"] = oth_stats[metric]["best"]["rating"]
            oth[metric_name + "_current"] = oth_stats[metric]["last"]["rating"] 
            oth[metric_name + "_wins"] = oth_stats[metric]["record"]["win"]   
            oth[metric_name + "_draws"] = oth_stats[metric]["record"]["draw"]              
            oth[metric_name + "_losses"] = oth_stats[metric]["record"]["loss"]

        if metric == "fide":
            u["FIDE"] = u_stats["fide"]
            oth["FIDE"] = oth_stats["fide"]
        
        if metric == "puzzle_rush":
            u[metric] = u_stats[metric]["best"]["score"]
            oth[metric] = oth_stats[metric]["best"]["score"]

        if metric == "tactics":
            u["puzzles_best_rating"] = u_stats[metric]["highest"]["rating"]
            oth["puzzles_best_rating"] = oth_stats[metric]["highest"]["rating"]

    return pd.DataFrame.from_dict(stats, orient="columns")


def expand_data(df: pd.DataFrame) -> pd.DataFrame:
    cols = df.columns.to_list()
    user, other = cols[0], cols[1]
    unwanted_labels = {"FIDE", "puzzle_rush", "puzzles_best_rating"}
    current_labels = set(df.index.to_list())
    labels_to_exlcude = unwanted_labels.intersection(current_labels)
    filt_df = df.drop(labels_to_exlcude)
    for s in ["wins", "draws", "losses"]:
        temp_df = filt_df.filter(like=s, axis=0)
        a, b = temp_df[user].sum(), temp_df[other].sum()
        df.loc[f"total_{s}"] = [a, b]
    u_games, oth_games = filt_df[user].sum(), filt_df[other].sum()
    df.loc['total_games'] = [u_games, oth_games]
    return df


