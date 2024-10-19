import pytest
import pandas as pd
import numpy as np
from json import load
from unittest.mock import patch
from helpers.classes import ChessUser, Comparison


with open("test/test_data/test_aporian_profile.json", "r") as file:
    aporian_profile = load(file)

with open("test/test_data/test_aporian_stats.json", "r") as file:
    aporian_stats = load(file)

with open("test/test_data/test_flannel_profile.json", "r") as file:
    flannel_profile = load(file)

with open("test/test_data/test_flannel_stats.json", "r") as file:
    flannel_stats = load(file)


@pytest.fixture(scope="function")
@patch("helpers.classes.get_stats")
@patch("helpers.classes.get_profile")
def test_aporian(mock_get_profile, mock_get_stats):
    mock_get_profile.return_value = aporian_profile
    mock_get_stats.return_value = aporian_stats
    test_a = ChessUser("Aporian")
    test_a.add_stats()
    return test_a


@pytest.fixture(scope="function")
@patch("helpers.classes.get_stats")
@patch("helpers.classes.get_profile")
def test_flannel(mock_get_profile, mock_get_stats):
    mock_get_profile.return_value = flannel_profile
    mock_get_stats.return_value = flannel_stats
    test_f = ChessUser("FlannelMind")
    test_f.add_stats()
    return test_f


@pytest.fixture()
def test_comparison(test_aporian, test_flannel):
    comp = Comparison(test_aporian, test_flannel)
    return comp


class TestInstantiationAttributes:
    @pytest.mark.it("Instantiates with passed ChessUser objects as user and other attributes")
    def test_instantiates_with_chess_users(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        assert test_comparison.user == test_aporian
        assert test_comparison.other == test_flannel

    @pytest.mark.it("Instantiates with intersection of available metrics as comparable_metric attribute")
    def test_instantiates_with_comparable_metrics(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        expected_intersection = test_aporian.available_metrics.intersection(test_flannel.available_metrics)
        assert test_comparison.comparable_metrics == expected_intersection

    @pytest.mark.it("Instantiates with dataframe as df attribute")
    def test_instantiates_with_dfs(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        assert isinstance(test_comparison.df , pd.DataFrame)

class TestCreateDF:
    @pytest.mark.it("Df has passed user and other names as column names")
    def test_data_frame_has_expected_col_names(self, test_comparison):
        expected_cols = ['Aporian', 'FlannelMind']
        assert test_comparison.df.columns.to_list() == expected_cols

    @pytest.mark.it("Df has metrics available for both users (only) as indices")
    def test_data_frame_has_expected_row_names(self, test_comparison):
        expected_rows = [
            "blitz_best",
            "blitz_current",
            "blitz_wins",
            "blitz_draws",
            "blitz_losses",
            "daily_best",
            "daily_current",
            "daily_wins",
            "daily_draws",
            "daily_losses",
            "rapid_best",
            "rapid_current",
            "rapid_wins",
            "rapid_draws",
            "rapid_losses",
            "puzzle_rush",
            "puzzles",
        ]
        output_rows = test_comparison.df.index.to_list()
        assert set(expected_rows) == set(output_rows)

    @pytest.mark.it("Df populates rows with expected data from passed ChessUsers")
    def test_row_data(self, test_comparison):
        expected_values = {
            "puzzles": [2593, 1808],
            "daily_best": [1584, 1278],
            "rapid_wins": [72, 2111],
        }
        for k, v in expected_values.items():
            assert test_comparison.df.loc[k].tolist() == v


class TestAddGameTotals:
    def test_adds_total_wins(self, test_comparison):
        test_comparison.add_game_totals()
        expected = [384, 2424]
        actual = test_comparison.df.loc["total_wins"].to_list()
        assert actual == expected

    def test_adds_total_draws(self, test_comparison):
        test_comparison.add_game_totals()
        expected = [15, 204]
        actual = test_comparison.df.loc["total_draws"].to_list()
        assert actual == expected

    def test_adds_total_losses(self, test_comparison):
        test_comparison.add_game_totals()
        expected = [366, 2434]
        actual = test_comparison.df.loc["total_losses"].to_list()
        assert actual == expected

    def test_adds_total_games(self, test_comparison):
        test_comparison.add_game_totals()
        expected = [765, 5062]
        actual = test_comparison.df.loc["total_games"].to_list()
        assert actual == expected

    def test_adds_totals_to_component_objects_as_attributes(self, test_comparison):
        test_comparison.add_game_totals()
        # user
        assert test_comparison.user.total_wins
        assert test_comparison.user.total_draws
        assert test_comparison.user.total_losses
        assert test_comparison.user.total_games
        # other
        assert test_comparison.other.total_wins
        assert test_comparison.other.total_draws
        assert test_comparison.other.total_losses
        assert test_comparison.other.total_games


class TestAddAvgRating:
    def test_adds_avg_rating_index_to_df(self, test_comparison):
        test_comparison.add_avg_rating()
        indices = test_comparison.df.index.to_list()
        assert "avg_rating_current" in indices

    def test_calculates_avg_rating_from_available_ratings(self, test_comparison):
        test_comparison.add_avg_rating()
        aporian_expected_avg = int(np.mean([1508, 1222, 1012]))
        flannel_expected_avg = int(np.mean([882, 944, 798]))
        aporian_avg = test_comparison.df.at["avg_rating_current", "Aporian"]
        flannel_avg = test_comparison.df.at["avg_rating_current", "FlannelMind"]
        assert aporian_avg == aporian_expected_avg
        assert flannel_avg == flannel_expected_avg


# class TestGetHeadToHead:
#     def test_returns_dataframe(self, expanded_df):
#         output = get_head_to_head(expanded_df)
#         print(output)
#         assert isinstance(output, pd.DataFrame)

#     @pytest.mark.it("Df has passed user and other names as column names")
#     def test_data_frame_has_expected_col_names(self, expanded_df):
#         df = get_head_to_head(expanded_df)
#         expected_cols = ["Mazza", "Cazza", "Your points", "Their points"]
#         assert expected_cols == df.columns.to_list()
