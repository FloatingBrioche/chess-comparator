from json import load
from unittest.mock import patch

import pytest
import pandas as pd
import numpy as np

from classes.chess_user import ChessUser
from classes.comparison import Comparison


### Test Data ###


with open("test/test_data/test_aporian_profile.json", "r") as file:
    aporian_profile = load(file)

with open("test/test_data/test_aporian_stats.json", "r") as file:
    aporian_stats = load(file)

with open("test/test_data/test_flannel_profile.json", "r") as file:
    flannel_profile = load(file)

with open("test/test_data/test_flannel_stats.json", "r") as file:
    flannel_stats = load(file)


### Fixtures ###


@pytest.fixture(scope="function")
@patch("classes.chess_user.get_stats")
@patch("classes.chess_user.get_profile")
def test_aporian(mock_get_profile, mock_get_stats):
    mock_get_profile.return_value = aporian_profile
    mock_get_stats.return_value = aporian_stats
    test_a = ChessUser("Aporian")
    test_a.add_stats()
    return test_a


@pytest.fixture(scope="function")
@patch("classes.chess_user.get_stats")
@patch("classes.chess_user.get_profile")
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


### Tests ###


class TestInstantiationAttributes:
    @pytest.mark.it(
        "Instantiates with passed ChessUser objects as user and other attributes"
    )
    def test_instantiates_with_chess_users(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        assert test_comparison.user == test_aporian
        assert test_comparison.other == test_flannel

    @pytest.mark.it(
        "Instantiates with intersection of available metrics as comparable_metric attribute"
    )
    def test_instantiates_with_comparable_metrics(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        expected_intersection = test_aporian.available_metrics.intersection(
            test_flannel.available_metrics
        )
        assert test_comparison.comparable_metrics == expected_intersection

    @pytest.mark.it("Instantiates with dataframe as df attribute")
    def test_instantiates_with_dfs(self, test_aporian, test_flannel):
        test_comparison = Comparison(test_aporian, test_flannel)
        assert isinstance(test_comparison.df, pd.DataFrame)


class TestCreateDF:
    @pytest.mark.it("Df has passed user and other names as column names")
    def test_data_frame_has_expected_col_names(self, test_comparison):
        expected_cols = ["Aporian", "FlannelMind"]
        assert test_comparison.df.columns.to_list() == expected_cols

    @pytest.mark.it("Df has metrics available for both users (only) as indices")
    def test_data_frame_has_expected_row_names(self, test_comparison):
        expected_rows = [
            "blitz_best",
            "daily_draw_%",
            "blitz_draws",
            "blitz_loss_%",
            "puzzles",
            "rapid_total_games",
            "rapid_loss_%",
            "daily_draws",
            "blitz_losses",
            "daily_loss_%",
            "daily_losses",
            "rapid_best",
            "blitz_wins",
            "rapid_draws",
            "blitz_draw_%",
            "rapid_current",
            "blitz_total_games",
            "rapid_draw_%",
            "daily_best",
            "blitz_win_%",
            "rapid_losses",
            "daily_win_%",
            "daily_total_games",
            "rapid_wins",
            "rapid_win_%",
            "daily_wins",
            "daily_current",
            "puzzle_rush",
            "blitz_current",
            "FIDE",
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

    def test_adds_overall_win_loss_percentages(self, test_comparison):
        test_comparison.add_game_totals()
        indices = test_comparison.df.index.to_list()
        assert "overall_win_%" in indices
        assert "overall_loss_%" in indices


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


class TestGetHeadToHead:
    def test_returns_dataframe(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        output = test_comparison.get_head_to_head()
        assert isinstance(output, pd.DataFrame)

    @pytest.mark.it("Returns new df object - not self.df")
    def test_return_distinct_df(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        output = test_comparison.get_head_to_head()
        assert output is not test_comparison.df

    @pytest.mark.it("Df has 'Your points' and 'Their points' column")
    def test_data_frame_has_expected_col_names(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        output = test_comparison.get_head_to_head()
        expected_cols = ["Aporian", "FlannelMind", "Your points", "Their points"]
        assert expected_cols == output.columns.to_list()

    @pytest.mark.it("Sets total_points attribute for component ChessUser objects")
    def test_sets_total_points_attributes(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        assert not test_comparison.user.total_points
        assert not test_comparison.other.total_points
        test_comparison.get_head_to_head()
        assert test_comparison.user.total_points
        assert test_comparison.other.total_points

    @pytest.mark.it("Awards points to the user with lowest loss_%")
    def test_points_lowest_loss(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        loss_df = df.filter(regex="loss_%", axis=0)
        for row in loss_df.itertuples(index=False, name=None):
            user_has_lower_loss_pc = row[0] < row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_lower_loss_pc == user_is_given_point
            other_has_lower_loss_pc = row[0] > row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_lower_loss_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with highest win_%")
    def test_points_highest_win(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        win_df = df.filter(regex="win_%", axis=0)
        for row in win_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with higher current rating")
    def test_points_higher_current(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        current_df = df.filter(regex="current", axis=0)
        for row in current_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with higher best rating")
    def test_points_higher_best(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        loss_df = df.filter(regex="best", axis=0)
        for row in loss_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with higher puzzle rating")
    def test_points_higher_puzzle(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        loss_df = df.filter(regex="puzzle", axis=0)
        for row in loss_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with higher FIDE rating")
    def test_points_higher_fide(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        loss_df = df.filter(regex="FIDE", axis=0)
        for row in loss_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Awards points to the user with higher total games")
    def test_points_higher_total_games(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        loss_df = df.filter(regex="total_games", axis=0)
        for row in loss_df.itertuples(index=False, name=None):
            user_has_higher_win_pc = row[0] > row[1]
            user_is_given_point = row[2] > row[3]
            assert user_has_higher_win_pc == user_is_given_point
            other_has_higher_win_pc = row[0] < row[1]
            other_is_given_point = row[2] < row[3]
            assert other_has_higher_win_pc == other_is_given_point

    @pytest.mark.it("Only includes indices where a point has been awarded")
    def test_includes_specific_indices(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        num_rows = len(df.index)
        num_points = df[["Your points", "Their points"]].to_numpy().sum()
        assert num_rows == num_points

    @pytest.mark.it("Sets winner attribute to component object with highest points")
    def test_sets_winner(self, test_comparison):
        test_comparison.add_game_totals()
        test_comparison.add_avg_rating()
        df = test_comparison.get_head_to_head()
        assert test_comparison.user.total_points > test_comparison.other.total_points
        assert test_comparison.winner == test_comparison.user
