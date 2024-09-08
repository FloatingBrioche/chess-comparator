import pandas as pd


def get_current_v_best(user_stats):
    stats = {"current": {}, "best": {}}
    for k, v in user_stats.items():
        if "last" in v:
            if "rating" in v["last"]:
                stats["current"][k] = v["last"]["rating"]
        if "best" in v:
            if "rating" in v["best"]:
                stats["best"][k] = v["best"]["rating"]
    return pd.DataFrame.from_dict(stats, orient="index")


# def get_current_v_best(user_stats):
#     current_stats = {}
#     best_stats = {}
#     for k,v in user_stats.items():
#         if "last" in v:
#             if "rating" in v["last"]:
#                 current_stats[k] = [v['last']['rating']]
#         if "best" in v:
#             if "rating" in v["best"]:
#                 best_stats[k] = [v['best']['rating']]
#     current_df = pd.DataFrame(data=current_stats, index=["Current"])
#     best_df = pd.DataFrame(data=best_stats, index=["Best"])
#     return pd.concat([current_df, best_df])
