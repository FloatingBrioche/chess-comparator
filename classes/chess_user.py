import pandas as pd
import asyncio
import httpx

from helpers.loggers import data_logger
from helpers.request_helpers import get_profile, get_stats, get_archives, get_archive


class ChessUser:
    """
    A Chess.com user

    This object holds information about the user and is used as a component
    object of the "Comparison" class. It instantiates with some
    attributes set to None that are later updated either via its own methods
    or those of the aggregate class.

    Attributes:
        username [str]:  the user's username
        profile [dict]: the user's profile information retrived via API
        name [None/str]: the user's name (if available)
        stats [None/dict]: the user's chess stats retrieved via API
        available_metrics [None/set]: the metrics (keys) included in the stats dict
        country [None/str]: the 2-character ISO 3166 code of the user's country
        total_wins [int]: the user's wins as calculated by add_game_totals
        total_draws [int]: the user's draws as calculated by add_game_totals
        total_losses [int]: the user's losses as calculated by add_game_totals
        total_games [int]: the user's games as calculated by add_game_totals
        total_points [None/int]: the user's points as calculated by get_head_to_head
    """

    def __init__(self, username: str):
        """
        Initialises the instance using the passed username string.

        The get_profile function is called during instantiation to attempt
        to retrieve the Chess.com profile for the user. For invalid usernames
        where no profile exists, the return value will be None.

        Args:
            username [str]: should be a chess.com username
        """

        self.username = username
        self.profile = get_profile(username)
        self.name = None
        self.stats = None
        self.available_metrics = None
        self.country = None
        self.total_points = None

    def add_stats(self) -> None:
        """
        Updates some instance attributes once the username has been validated.

        Calls the get_stats function, which sends a get request to
        the Chess.com API and converts the JSON response to a dictionary.
        """
        self.name = self.profile["name"] if self.profile.get("name") else self.username
        self.stats = get_stats(self.username)
        self.available_metrics = set(self.stats.keys())
        self.country = self.profile["country"].split("/")[-1]

    def get_current_v_best(self) -> pd.DataFrame:
        """
        Returns a dataframe with columns for the user's current and best ratings.

        Iterates over the instance's stats attribute and populates
        two accumalor dictionaries with relevant values, which are then
        used to create the dataframe.

        Args:
            N/A

        Returns:
            Dataframe with "Current" and "Best" columns and rows for each game type.

        Raises:
            KeyError: KeyErrors are caught and logged before being re-raised.
            TypeError: TypeErrors are caught and logged before being re-raised.
        """

        try:
            stats = {"current": {}, "best": {}}
            for k, v in self.stats.items():
                if isinstance(v, dict):
                    if "last" in v:
                        if "rating" in v["last"]:
                            stats["current"][k.removeprefix("chess_")] = v["last"][
                                "rating"
                            ]
                    if "best" in v:
                        if "rating" in v["best"]:
                            stats["best"][k.removeprefix("chess_")] = v["best"][
                                "rating"
                            ]
            return pd.DataFrame.from_dict(stats, orient="columns")
        except KeyError as e:
            data_logger.error(
                f"Key error in get_current_v_best: {str(e)}, key = {k}, value = {v}"
            )
            raise e
        except TypeError as e:
            data_logger.error(
                f"Type error in get_current_v_best: {str(e)}, key = {k}, value = {v}"
            )
            raise e

    async def get_game_history(self):
        async with httpx.AsyncClient() as client:
            archives = get_archives(self.username)
            tasks = [get_archive(url, client) for url in archives]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        monthly_archives = [result for result in results if isinstance(result, list)]
        failures = [result for result in results if not isinstance(result, list)]
        self.game_history = [y for x in monthly_archives for y in x]
    
    def wrangle_game_history_df(self):
        ids = []
        
        accumulator = {
            "colour": [],
            "time_class": [],
            "time_control": [],
            "rated": [],
            "rating": [],
            "opponent": [],
            "op_rating": [],
            "result": [], 
            "result_type": [],
            "eco": [],
            "accuracy": [],
            "op_accuracy": []
        }

        # https://www.chess.com/news/view/published-data-api#game-results
        draws = ["stalemate", "agreed", "repetition", "50move", "timevsinsufficient", "insufficient"]
        losses = ["checkmated", "timeout", "resigned", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]

        for game in self.game_history:
            ids.append(game["url"].split("/")[-1])

            accumulator["time_class"].append(game["time_class"])
            accumulator["time_control"].append(game["time_control"])
            accumulator["rated"].append(game["rated"])
            accumulator["eco"].append(game["eco"].split("/")[-1])

            white, black = game['white'], game['black']
            accuracies = game.get("accuracies", None)

            if white["username"] == self.username:
                accumulator["colour"].append("white")
                accumulator["rating"].append(white['rating'])
                accumulator["opponent"].append(black['username'])
                accumulator["op_rating"].append(black['rating'])
                accumulator["accuracy"].append(accuracies['white'] if accuracies else None)
                accumulator["op_accuracy"].append(accuracies['black'] if accuracies else None)
                if white['result'] == 'win':
                    accumulator["result"].append("win")
                    accumulator["result_type"].append(black['result'])
                elif white['result'] in draws:
                    accumulator["result"].append("draw")
                    accumulator["result_type"].append(white['result'])
                else:
                    accumulator["result"].append("loss")
                    accumulator["result_type"].append(white['result'])

            else:
                accumulator["colour"].append("black")
                accumulator["rating"].append(black['rating'])
                accumulator["opponent"].append(white['username'])
                accumulator["op_rating"].append(white['rating'])
                accumulator["accuracy"].append(accuracies['black'] if accuracies else None)
                accumulator["op_accuracy"].append(accuracies['white'] if accuracies else None)                
                if black['result'] == 'win':
                    accumulator["result"].append("win")
                    accumulator["result_type"].append(white['result'])
                elif black['result'] in draws:
                    accumulator["result"].append("draw")
                    accumulator["result_type"].append(black['result'])
                else:
                    accumulator["result"].append("loss")
                    accumulator["result_type"].append(black['result'])
        
        self.game_history_df = pd.DataFrame(accumulator, index=ids)

        return self.game_history_df

    def add_accuracy_stats(self):
        accuracies = self.game_history_df['accuracy']
        
        avg_accuracy = accuracies.mean()
        highest_accuracy = accuracies.max()
        lowest_accuracy = accuracies.min()
        
        self.avg_accuracy = round(avg_accuracy, 2)
        self.highest_accuracy = highest_accuracy
        self.lowest_accuracy = lowest_accuracy
