import pandas as pd
from helpers.loggers import data_logger
from helpers.request_helpers import get_profile, get_stats


class ChessUser:
    def __init__(self, username):
        self.username = username
        self.profile = get_profile(username)
        self.name = None
        self.stats = None
        self.available_metrics = None
        self.country = None

    def add_stats(self) -> None:
        self.name = self.profile["name"] if self.profile.get("name") is not None else self.username
        self.stats = get_stats(self.username)
        self.available_metrics = set(self.stats.keys())
        self.country = self.profile["country"].split("/")[-1]

    def get_current_v_best(self) -> pd.DataFrame:
        try:
            stats = {"current": {}, "best": {}}
            for k, v in self.stats.items():
                if isinstance(v, dict):
                    if "last" in v:
                        if "rating" in v["last"]:
                            stats["current"][k.removeprefix("chess_")] = v["last"]["rating"]
                    if "best" in v:
                        if "rating" in v["best"]:
                            stats["best"][k.removeprefix("chess_")] = v["best"]["rating"]
            return pd.DataFrame.from_dict(stats, orient="columns")
        except KeyError as e:
            data_logger.error(f"Key error in get_current_v_best: {str(e)}, key = {k}, value = {v}")
            raise e
        except TypeError as e:
            data_logger.error(f"Type error in get_current_v_best: {str(e)}, key = {k}, value = {v}")
            raise e
    

class Comparison:
    def __init__(self, user, other):
        self.user = user
        self.other = other
        self.comparable_metrics = user.available_metrics & other.available_metrics
        self.df = None
        self.create_df()


    def create_df(self):
        try:
            # Acceses usernames for dict keys and create new keys in stats dict
            stats = {self.user.username: {}, self.other.username: {}}

            # Shorthand alias variables
            u, oth = stats[self.user.username], stats[self.other.username]
            u_stats, oth_stats = self.user.stats, self.other.stats

            # Iterates over common metrics, looks up values and adds k-vs to stats dict
            for metric in self.comparable_metrics:
                
                metric_name = metric.removeprefix("chess_")
                
                if metric == "fide":
                    u["FIDE"] = u_stats["fide"]
                    oth["FIDE"] = oth_stats["fide"]

                elif metric == "puzzle_rush":
                    if "best" in u_stats[metric] and "best" in oth_stats[metric]:
                        u[metric] = u_stats[metric]["best"]["score"]
                        oth[metric] = oth_stats[metric]["best"]["score"]

                elif metric == "tactics":
                    if "highest" in u_stats[metric] and "highest" in oth_stats[metric]:
                        u["puzzles"] = u_stats[metric]["highest"]["rating"]
                        oth["puzzles"] = oth_stats[metric]["highest"]["rating"]
                
                elif "record" in u_stats[metric]:                
                    u[metric_name + "_current"] = u_stats[metric]["last"]["rating"]
                    u[metric_name + "_wins"] = u_stats[metric]["record"]["win"]
                    u[metric_name + "_draws"] = u_stats[metric]["record"]["draw"]
                    u[metric_name + "_losses"] = u_stats[metric]["record"]["loss"]
                    
                    oth[metric_name + "_current"] = oth_stats[metric]["last"]["rating"]
                    oth[metric_name + "_wins"] = oth_stats[metric]["record"]["win"]
                    oth[metric_name + "_draws"] = oth_stats[metric]["record"]["draw"]
                    oth[metric_name + "_losses"] = oth_stats[metric]["record"]["loss"]

                    if "best" in u_stats[metric] and "best" in oth_stats[metric]:
                        u[metric_name + "_best"] = u_stats[metric]["best"]["rating"]
                        oth[metric_name + "_best"] = oth_stats[metric]["best"]["rating"]

            # Converts stats dict to dataframe with usernames as  columns
            self.df = pd.DataFrame.from_dict(stats, orient="columns")
        
        except KeyError as e:
            data_logger.error(f"Key error in get_user_v_other: {str(e)}, metric = {metric}, username = {self.user.username}, other_username = {self.other.username}")
            raise e
        
        except TypeError as e:
            data_logger.error(f"Type error in get_user_v_other: {str(e)}, metric = {metric}, username = {self.user.username}, other_username = {self.other.username}")
            raise e
        

    def add_game_totals(self):
        try:
            # Captures usernames/df cols
            user, other = self.user.username, self.other.username

            # Creates and iterates over filtered df to calculate total ws, ds, ls
            filt_df = self.df.filter(regex="_wins|_draws|_losses", axis=0)
            for s in ["wins", "draws", "losses"]:
                temp_df = filt_df.filter(like=s, axis=0)
                a, b = temp_df[user].sum(), temp_df[other].sum()
                self.df.loc[f"total_{s}"] = [a, b]
                setattr(self.user, f"total_{s}", a)
                setattr(self.other, f"total_{s}", b)

            # Creates total games index
            u_games, oth_games = filt_df[user].sum(), filt_df[other].sum()
            self.df.loc["total_games"] = [u_games, oth_games]
            setattr(self.user, "total_games", u_games)
            setattr(self.other, "total_games", oth_games)
        
        except (KeyError, TypeError) as e:
            data_logger.error(f"Error in add_game_totals: {str(e)}")
            raise e
    

    def add_avg_rating(self):
        try:
            filt_df = self.df.filter(regex="current", axis=0)
            u_avg = filt_df[self.user.username].mean()
            oth_avg = filt_df[self.other.username].mean()
            self.df.loc["avg_rating_current"] = [int(u_avg), int(oth_avg)]
        except KeyError as e:
            data_logger.error(f"Error in add_avg_rating: {str(e)}")
            raise e
        

    def add_win_loss_percentages(self):
        u_name = self.user.username
        o_name = self.other.username
        try:
            u_win_pc = round((self.user.total_wins / self.user.total_games) * 100, 2)
            u_loss_pc = round((self.user.total_losses / self.user.total_games) * 100, 2)

            o_win_pc = round((self.other.total_wins / self.other.total_games) * 100, 2)
            o_loss_pc = round((self.other.total_losses / self.other.total_games) * 100, 2)

            self.df.loc[f"overall_win_%"] = [u_win_pc, o_win_pc]
            self.df.loc[f"overall_loss_%"] = [u_loss_pc, o_loss_pc]
                        
            game_types = ["blitz", "bullet", "daily", "rapid", "chess960"]
            
            for game in game_types:
                filt_df = self.df.filter(regex=f"^{game}_[a-z]+", axis=0)
                if not filt_df.empty:
                    # User
                    u_wins = filt_df.at[f"{game}_wins", u_name]
                    u_draws = filt_df.at[f"{game}_draws", u_name]
                    u_losses = filt_df.at[f"{game}_losses", u_name]
                    u_total_games = u_wins + u_draws + u_losses
                    u_win_pc = round((u_wins / u_total_games) * 100, 2)
                    u_loss_pc = round((u_losses / u_total_games) * 100, 2)

                    # Other
                    o_wins = filt_df.at[f"{game}_wins", o_name]
                    o_draws = filt_df.at[f"{game}_draws", o_name]
                    o_losses = filt_df.at[f"{game}_losses", o_name]
                    o_total_games = o_wins + o_draws + o_losses
                    o_win_pc = round((o_wins / o_total_games) * 100, 2)
                    o_loss_pc = round((o_losses / o_total_games) * 100, 2)

                    self.df.loc[f"{game}_win_%"] = [u_win_pc, o_win_pc]
                    self.df.loc[f"{game}_loss_%"] = [u_loss_pc, o_loss_pc]

        except KeyError as e:
            data_logger.error(f"Error in add_win_loss_percentages: {str(e)}")
            raise e
            

    def get_head_to_head(self) -> pd.DataFrame:
        u_points = []
        o_points = []
        
        for row in self.df.iterrows():
            index = row[0]
            values = row[1].tolist()
            pos_metric = any([
                "wins" in index, 
                "current" in index, 
                "best" in index,
                "puzzle" in index,
                "FIDE" in index
                ])
            neg_metric = "losses" in index
            
            if pos_metric:
                if values[0] > values[1]:
                    u_points.append(1)
                    o_points.append(0)
                elif values[0] < values[1]:
                    u_points.append(0)
                    o_points.append(1)
                else:
                    u_points.append(0)
                    o_points.append(0)
            
            elif neg_metric:
                if values[0] < values[1]:
                    u_points.append(1)
                    o_points.append(0)
                elif values[0] > values[1]:
                    u_points.append(0)
                    o_points.append(1)
                else:
                    u_points.append(0)
                    o_points.append(0)
            
            else:
                u_points.append(0)
                o_points.append(0)
        
        self.df['Your points'] = u_points
        self.df['Their points'] = o_points
        self.df.loc[' '] = [' ', ' ', ' ', ' ']
        self.df.loc["Total points"] = [' ', ' ', sum(u_points), sum(o_points)]
        
        return self.df