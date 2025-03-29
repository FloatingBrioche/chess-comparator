import time
from unittest.mock import patch
from json import load
from itertools import combinations

import pytest
import pandas as pd

from classes.chess_user import ChessUser
from helpers.vars import (
    required_game_archive_keys,
    test_monthly_archives_small,
    test_monthly_archives_large,
)


# Fixtures


@pytest.fixture()
def profile():
    with open("test/test_data/test_aporian_profile.json", "r") as file:
        profile = load(file)
    return profile


@pytest.fixture()
def aporian_stats():
    with open("test/test_data/test_aporian_stats.json", "r") as file:
        user_stats = load(file)
    return user_stats


@pytest.fixture(scope="function")
def aporian_game_history():
    with open(
        "test/test_data/test_aporian_game_history.json", "r", encoding="utf8"
    ) as f:
        aporian_game_history = load(f)
    return aporian_game_history


@pytest.fixture(scope="function")
@patch("classes.chess_user.get_profile")
def TestAporian(mock_get_profile, profile):
    mock_get_profile.return_value = profile
    return ChessUser("Aporian")


@pytest.fixture(scope="function")
@patch("classes.chess_user.get_stats")
@patch("classes.chess_user.get_profile")
def TestAporianStatsAdded(mock_get_profile, mock_get_stats, profile, aporian_stats):
    mock_get_profile.return_value = profile
    mock_get_stats.return_value = aporian_stats
    TestAporianStatsAdded = ChessUser("Aporian")
    TestAporianStatsAdded.add_stats()
    return TestAporianStatsAdded


@pytest.fixture(scope="function")
@patch("classes.chess_user.get_stats")
@patch("classes.chess_user.get_profile")
def test_aporian_w_game_history(
    mock_get_profile, mock_get_stats, profile, aporian_stats, aporian_game_history
):
    mock_get_profile.return_value = profile
    mock_get_stats.return_value = aporian_stats
    test_aporian_w_game_history = ChessUser("Aporian")
    test_aporian_w_game_history.add_stats()
    test_aporian_w_game_history.game_history = aporian_game_history
    return test_aporian_w_game_history


@pytest.fixture(scope="function")
def test_aporian_w_game_history_df(test_aporian_w_game_history):
    test_aporian_w_game_history.wrangle_game_history_df()
    return test_aporian_w_game_history


# Tests


class TestInstantiationAttributes:
    @pytest.mark.it("Instantiates with passed string as username attribute")
    def test_instantiates_with_username(self, TestAporian):
        assert TestAporian.username == "Aporian"

    @pytest.mark.it("Instantiates with profile as None if passed invalid username")
    def test_instantiates_with_profile_as_none(self):
        invalid_user = ChessUser("AporianGkd98")
        assert invalid_user.profile is None

    @pytest.mark.it("Instantiates with profile as dict if passed valid username")
    def test_instantiates_with_profile_dict(self, TestAporian):
        assert isinstance(TestAporian.profile, dict)

    @pytest.mark.it("Instantiates with name attribute as None")
    def test_instantiates_with_name_none(self, TestAporian):
        assert TestAporian.name is None

    @pytest.mark.it("Instantiates with stats attribute as None")
    def test_instantiates_with_stats_none(self, TestAporian):
        assert TestAporian.stats is None

    @pytest.mark.it("Instantiates with country attribute as None")
    def test_instantiates_with_stats_none(self, TestAporian):
        assert TestAporian.country is None

    @pytest.mark.it("Instantiates with available_metrics attribute as None")
    def test_instantiates_with_available_metrics_none(self, TestAporian):
        assert TestAporian.available_metrics is None


class TestAddStats:
    @pytest.mark.it("Updates name att to profile name if profile contains name")
    @patch("classes.chess_user.get_stats")
    def test_updates_profile_name(self, mock_get_stats, TestAporian):
        TestAporian.add_stats()
        assert TestAporian.name == "Martin C."

    @pytest.mark.it("Updates name att to username if profile doesn't contain name")
    @patch("classes.chess_user.get_stats")
    @patch("classes.chess_user.get_profile")
    def test_updates_name_username(self, mock_get_profile, mock_get_stats, profile):
        del profile["name"]
        mock_get_profile.return_value = profile
        TestAporianNoName = ChessUser("Aporian")
        TestAporianNoName.add_stats()
        assert TestAporianNoName.name == "Aporian"

    @pytest.mark.it("Updates stats attribute with dictionary")
    @patch("classes.chess_user.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.stats is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.stats, dict)

    @pytest.mark.it("Updates country attribute with country code string")
    @patch("classes.chess_user.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.country is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.country, str)
        assert TestAporian.country == "XE"

    @pytest.mark.it("Updates available_metrics attribute with set")
    @patch("classes.chess_user.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.available_metrics is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.available_metrics, set)

    @pytest.mark.it("Available_metrics is set of stats keys")
    @patch("classes.chess_user.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        TestAporian.add_stats()
        assert set(aporian_stats.keys()) == TestAporian.available_metrics

    class TestCurrentVsBest:
        def test_returns_data_frame(self, TestAporianStatsAdded):
            result = TestAporianStatsAdded.get_current_v_best()
            assert isinstance(result, pd.DataFrame)

        @pytest.mark.it("Df has 'current' and 'best' as column names")
        def test_data_frame_has_expected_col_names(self, TestAporianStatsAdded):
            df = TestAporianStatsAdded.get_current_v_best()
            expected_cols = ["current", "best"]
            output_cols = df.columns.to_list()
            assert expected_cols == output_cols

        @pytest.mark.it("Df has game types as indices")
        def test_data_frame_has_expected_row_names(self, TestAporianStatsAdded):
            df = TestAporianStatsAdded.get_current_v_best()
            expected_rows = ["daily", "chess960_daily", "rapid", "bullet", "blitz"]
            output_rows = df.index.to_list()
            assert expected_rows == output_rows

    class TestGetGameHistory:
        @pytest.mark.it("Returns None")
        @pytest.mark.asyncio(loop_scope="function")
        @patch(
            "classes.chess_user.get_archives", return_value=test_monthly_archives_small
        )
        async def test_returns_None(self, MockGetArchives, TestAporian):
            result = await TestAporian.get_game_history()
            assert result is None

        @pytest.mark.it("Creates game_history attribute")
        @pytest.mark.asyncio(loop_scope="function")
        @patch(
            "classes.chess_user.get_archives", return_value=test_monthly_archives_small
        )
        async def test_updates_game_history_attribute(
            self, MockGetArchives, TestAporian
        ):
            assert "game_history" not in dir(TestAporian)
            await TestAporian.get_game_history()
            assert TestAporian.game_history

        @pytest.mark.it(
            "game_history attribute is list of game archives with required keys"
        )
        @pytest.mark.asyncio(loop_scope="function")
        @patch(
            "classes.chess_user.get_archives", return_value=test_monthly_archives_small
        )
        async def test_updates_game_history_attribute(
            self, MockGetArchives, TestAporian
        ):
            await TestAporian.get_game_history()
            game_history = TestAporian.game_history
            assert isinstance(game_history, list)
            for game in game_history:
                game_keys = set(game.keys())
                assert all([key in game_keys for key in required_game_archive_keys])

        @pytest.mark.it("Executes in <2 seconds for large set of archives")
        @pytest.mark.asyncio(loop_scope="function")
        @patch(
            "classes.chess_user.get_archives", return_value=test_monthly_archives_large
        )
        async def test_performant_execution(self, MockGetArchives, TestAporian):
            start = time.time()
            await TestAporian.get_game_history()
            end = time.time()
            execution_time = end - start
            print(f"Execution time = {execution_time:.2f}")
            print(f"Number of requests = {len(test_monthly_archives_large)}")
            assert execution_time < 2


class TestWrangleGameHistory:
    @pytest.mark.it("Returns data frame")
    def test_returns_df(self, test_aporian_w_game_history):
        output = test_aporian_w_game_history.wrangle_game_history_df()
        assert isinstance(output, pd.DataFrame)

    @pytest.mark.it("Length of df == length of game_history")
    def test_df_len(self, test_aporian_w_game_history):
        len_game_history = len(test_aporian_w_game_history.game_history)
        output = test_aporian_w_game_history.wrangle_game_history_df()
        assert output.shape[0] == len_game_history

    @pytest.mark.it("Has expected columns")
    def test_df_columns(self, test_aporian_w_game_history):
        output = test_aporian_w_game_history.wrangle_game_history_df()
        cols = output.columns.tolist()
        assert output.shape[1] == 14
        assert cols == [
            "colour",
            "time_class",
            "time_control",
            "rated",
            "rating",
            "opponent",
            "op_rating",
            "rating_differential",
            "result",
            "result_type",
            "eco",
            "accuracy",
            "op_accuracy",
            "url",
        ]

    @pytest.mark.it("Adds game_history_df attribute to object")
    def test_adds_game_df(self, test_aporian_w_game_history):
        assert "game_history_df" not in dir(test_aporian_w_game_history)
        output = test_aporian_w_game_history.wrangle_game_history_df()
        assert "game_history_df" in dir(test_aporian_w_game_history)
        assert isinstance(test_aporian_w_game_history.game_history_df, pd.DataFrame)


class TestAddAccuracyStats:
    @pytest.mark.it("Returns None")
    def test_returns_none(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.add_accuracy_stats()
        assert output is None

    @pytest.mark.it("Adds avg_accuracy attribute to object")
    def test_adds_avg_accuracy(self, test_aporian_w_game_history_df):
        assert "avg_accuracy" not in dir(test_aporian_w_game_history_df)
        output = test_aporian_w_game_history_df.add_accuracy_stats()
        assert "avg_accuracy" in dir(test_aporian_w_game_history_df)

    @pytest.mark.it("Adds highest_accuracy attribute to object")
    def test_adds_highest_accuracy(self, test_aporian_w_game_history_df):
        assert "highest_accuracy" not in dir(test_aporian_w_game_history_df)
        output = test_aporian_w_game_history_df.add_accuracy_stats()
        assert "highest_accuracy" in dir(test_aporian_w_game_history_df)

    @pytest.mark.it("Adds lowest_accuracy attribute to object")
    def test_adds_lowest_accuracy(self, test_aporian_w_game_history_df):
        assert "lowest_accuracy" not in dir(test_aporian_w_game_history_df)
        output = test_aporian_w_game_history_df.add_accuracy_stats()
        assert "lowest_accuracy" in dir(test_aporian_w_game_history_df)


class TestQueryGameHistory:
    @pytest.mark.it("Returns data frame")
    def test_returns_df(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.query_game_history(
            "accuracy", ["eco", "colour"]
        )
        assert isinstance(output, pd.DataFrame)

    @pytest.mark.it("Df uses passed 'dimension(s)' as index/MultiIndex")
    def test_df_has_expected_index(self, test_aporian_w_game_history_df):
        i_output = test_aporian_w_game_history_df.query_game_history(
            "accuracy", ["time_class"]
        )
        i_expected = ["time_class"]
        index = i_output.index.names
        assert index == i_expected

        mi_output = test_aporian_w_game_history_df.query_game_history(
            "accuracy", ["time_class", "colour"]
        )
        mi_expected = ["time_class", "colour"]
        multi_index = mi_output.index.names
        assert multi_index == mi_expected

    @pytest.mark.it(
        "If 'op_rating' in dimensions, rounds ratings to nearest 100th and groups them"
    )
    def test_df_op_rating(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.query_game_history(
            "accuracy", ["op_rating"]
        )
        ratings = output.index.to_list()
        assert all(rating % 100 == 0 for rating in ratings)

    @pytest.mark.it("If 'accuracy' selected as fact, df has 'accuracy' column")
    def test_df_has_accuracy_col(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.query_game_history(
            "accuracy", ["time_class", "colour"]
        )
        expected = ["accuracy"]
        col = output.columns.to_list()
        assert col == expected

    @pytest.mark.it("If 'result' selected as fact, df has win/draw/loss % columns")
    def test_df_has_result_cols(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.query_game_history(
            "result", ["op_rating"]
        )
        expected = ["win_pc", "draw_pc", "loss_pc"]
        assert output.columns.to_list() == expected

    @pytest.mark.it("If 'url' selected as fact, df has games_played column")
    def test_df_has_result_cols(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.query_game_history(
            "url", ["op_rating"]
        )
        expected = ["games_played"]
        assert output.columns.to_list() == expected

    @pytest.mark.it("Works for all possible combinations of accuracy and dimensions")
    def test_accuracy_combinations(self, test_aporian_w_game_history_df):
        dimensions = ["colour", "time_class", "op_rating", "result", "eco"]
        for x in range(1, len(dimensions) + 1):
            for combination in combinations(dimensions, x):
                test_aporian_w_game_history_df.query_game_history(
                    "accuracy", list(combination)
                )
                assert True

    @pytest.mark.it("Works for all possible combinations of url and dimensions")
    def test_url_combinations(self, test_aporian_w_game_history_df):
        dimensions = ["colour", "time_class", "op_rating", "result", "eco"]
        for x in range(1, len(dimensions) + 1):
            for combination in combinations(dimensions, x):
                test_aporian_w_game_history_df.query_game_history(
                    "url", list(combination)
                )
                assert True

    @pytest.mark.it(
        "Works for all possible combinations of result and dimensions (excluding result)"
    )
    def test_result_combinations(self, test_aporian_w_game_history_df):
        dimensions = ["colour", "time_class", "op_rating", "eco"]
        for x in range(1, len(dimensions) + 1):
            for combination in combinations(dimensions, x):
                test_aporian_w_game_history_df.query_game_history(
                    "result", list(combination)
                )
                assert True

class TestGetTop5:
    @pytest.mark.it("Returns data frame")
    def test_returns_df(self, test_aporian_w_game_history_df):
        output = test_aporian_w_game_history_df.get_top_5("rating_differential")
        assert isinstance(output, pd.DataFrame)