import pandas as pd

from helpers.loggers import data_logger


class Comparison:
    """
    A comparison between two Chess.com users

    The class uses the aggregation of two ChessUser instances to create a
    dataframe of comparable metrics and encapsulates several methods for
    expanding the data.

    Attributes:
        user [ChessUser]: the ChessUser instance of the main user of the app
        other [Chessuser]: the other user selected for the comparison
        comparable_metrics [set]: the intersection of the metrics for both users
        df [pd.Dataframe]: a dataframe of metrics with columns for each user
        winner [Int]: the component object with the most get_head_to_head points
    """

    def __init__(self, user, other):
        """
        Initialises the instance using the passed ChessUser instances.

        During initialisation, the intersection of available metrics from
        the two users is evaluated and create_df is called using that
        set of metrics.

        Args:
            user [ChessUser]: the ChessUser instance of the main app user
            other [Chessuser]: the other user selected for the comparison
        """

        self.user = user
        self.other = other
        self.comparable_metrics = user.available_metrics & other.available_metrics
        self.create_df()

    def create_df(self) -> None:
        """
        Creates df and saves to df attribute of instance.

        Iterates over the instance's comparable metrics and accesses
        values from the component objects' stats attributes to
        build up dictionary of metrics. This dictionary is then used to
        construct the dataframe.

        Args:
            N/A

        Returns:
            None

        Raises:
            KeyError: KeyErrors are caught and logged before being re-raised.
            TypeError: TypeErrors are caught and logged before being re-raised.
        """

        try:
            # Accumulator dictionary to create df from
            stats = {self.user.username: {}, self.other.username: {}}

            # Shorthand alias variables
            u, oth = stats[self.user.username], stats[self.other.username]
            u_stats, oth_stats = self.user.stats, self.other.stats

            # Iterates over common metrics, looks up values and adds k-vs to stats dict
            for metric in sorted(list(self.comparable_metrics)):

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
                    u[metric_name + "_wins"] = (
                        u_wins := u_stats[metric]["record"]["win"]
                    )
                    u[metric_name + "_draws"] = (
                        u_draws := u_stats[metric]["record"]["draw"]
                    )
                    u[metric_name + "_losses"] = (
                        u_losses := u_stats[metric]["record"]["loss"]
                    )
                    u[metric_name + "_total_games"] = (
                        u_total := u_wins + u_draws + u_losses
                    )
                    u[metric_name + "_win_%"] = int((u_wins / u_total) * 100)
                    u[metric_name + "_draw_%"] = int((u_draws / u_total) * 100)
                    u[metric_name + "_loss_%"] = int((u_losses / u_total) * 100)

                    oth[metric_name + "_current"] = oth_stats[metric]["last"]["rating"]
                    oth[metric_name + "_wins"] = (
                        o_wins := oth_stats[metric]["record"]["win"]
                    )
                    oth[metric_name + "_draws"] = (
                        o_draws := oth_stats[metric]["record"]["draw"]
                    )
                    oth[metric_name + "_losses"] = (
                        o_losses := oth_stats[metric]["record"]["loss"]
                    )
                    oth[metric_name + "_total_games"] = (
                        o_total := o_wins + o_draws + o_losses
                    )
                    oth[metric_name + "_win_%"] = int((o_wins / o_total) * 100)
                    oth[metric_name + "_draw_%"] = int((o_draws / o_total) * 100)
                    oth[metric_name + "_loss_%"] = int((o_losses / o_total) * 100)

                    if "best" in u_stats[metric] and "best" in oth_stats[metric]:
                        u[metric_name + "_best"] = u_stats[metric]["best"]["rating"]
                        oth[metric_name + "_best"] = oth_stats[metric]["best"]["rating"]

            # Converts stats dict to dataframe with usernames as columns
            # and saves as instance attribute
            self.df = pd.DataFrame.from_dict(stats, orient="columns")

        except KeyError as e:
            data_logger.error(
                (
                    f"Key error in get_user_v_other: {str(e)}, "
                    f"metric = {metric}, "
                    f"username = {self.user.username}, "
                    f"other_username = {self.other.username}"
                )
            )
            raise e

        except TypeError as e:
            data_logger.error(
                (
                    f"Type error in get_user_v_other: {str(e)}, "
                    f"metric = {metric}, "
                    f"username = {self.user.username}, "
                    f"other_username = {self.other.username}"
                )
            )
            raise e

    def add_game_totals(self) -> None:
        """
        Expands df with data for total games and win %

        Accesses number of wins, draws and losses for each game type and
        adds these to create rows for overall wins, draws, losses and games.
        Then, adds rows for overall win_% and loss_%. During execution also
        updates attributes values in the component objects of the comparison
        instance.

        Args:
            N/A

        Returns:
            None

        Raises:
            KeyError: KeyErrors are caught and logged before being re-raised.
            TypeError: TypeErrors are caught and logged before being re-raised.
        """
        try:
            # Captures usernames to access df cols
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

            u_win_pc = int((self.user.total_wins / self.user.total_games) * 100)
            u_loss_pc = int((self.user.total_losses / self.user.total_games) * 100)

            o_win_pc = int((self.other.total_wins / self.other.total_games) * 100)
            o_loss_pc = int((self.other.total_losses / self.other.total_games) * 100)

            self.df.loc["overall_win_%"] = [u_win_pc, o_win_pc]
            self.df.loc["overall_loss_%"] = [u_loss_pc, o_loss_pc]

        except (KeyError, TypeError) as e:
            data_logger.error(f"Error in add_game_totals: {str(e)}")
            raise e

    def add_avg_rating(self) -> None:
        """
        Expands df with average rating over all game types for each user.

        Filters df to all current ratings and then adds row with
        mean rating for each user.

        Args:
            N/A

        Returns:
            None

        Raises:
            KeyError: KeyErrors are caught and logged before being re-raised.
        """

        try:
            filt_df = self.df.filter(regex="current", axis=0)
            u_avg = filt_df[self.user.username].mean()
            oth_avg = filt_df[self.other.username].mean()
            self.df.loc["avg_rating_current"] = [int(u_avg), int(oth_avg)]
        except KeyError as e:
            data_logger.error(f"Key error in add_avg_rating: {str(e)}")
            raise e

    def get_head_to_head(self) -> pd.DataFrame:
        """
        Returns new dataframe with columns for head-to-head points.

        Copies existing comparison df and iterates over rows comparing
        metrics and awarding points to the user with the best metrics.
        Adds points columns for each user and filters the df to only
        include rows where points have been awarded.

        Also sets the "winner" attribute in the comparison instance and
        the total points attributes in the two component objects.

        Args:
            N/A

        Returns:
            pd.dataframe

        """

        u_points = []
        o_points = []

        head_to_head_df = self.df.copy()

        for row in head_to_head_df.iterrows():
            index = row[0]
            values = row[1].tolist()
            pos_metric = any(
                [
                    "win_%" in index,
                    "current" in index,
                    "best" in index,
                    "puzzle" in index,
                    "FIDE" in index,
                    "total_games" in index,
                ]
            )
            neg_metric = "loss_%" in index

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

        head_to_head_df["Your points"] = u_points
        head_to_head_df["Their points"] = o_points

        self.user.total_points = sum(u_points)
        self.other.total_points = sum(o_points)

        self.winner = (
            self.other
            if self.other.total_points > self.user.total_points
            else self.user
        )

        return head_to_head_df.query("`Your points` + `Their points` == 1")