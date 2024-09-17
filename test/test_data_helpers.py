import pytest
import pandas as pd
from json import load
from data_helpers import get_current_v_best, get_user_v_other


@pytest.fixture()
def profile():
    with open("test/test_data/test_profile.json", "r") as file:
        profile = load(file)
    return profile


@pytest.fixture()
def user_stats():
    with open("test/test_data/test_stats.json", "r") as file:
        user_stats = load(file)
    return user_stats


@pytest.fixture()
def other_stats():
    with open("test/test_data/test_other_stats.json", "r") as file:
        other_stats = load(file)
    return other_stats


class TestCurrentVBest:
    def test_returns_data_frame(self, user_stats):
        result = get_current_v_best(user_stats)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it("Df has 'current' and 'best' as column names")
    def test_data_frame_has_expected_col_names(self, user_stats):
        df = get_current_v_best(user_stats)
        expected_cols = ["current", "best"]
        output_cols = df.columns.to_list()
        assert expected_cols == output_cols

    @pytest.mark.it("Df has game types as indices")
    def test_data_frame_has_expected_row_names(self, user_stats):
        df = get_current_v_best(user_stats)
        expected_rows = ["daily", "chess960_daily", "rapid", "bullet", "blitz"]
        output_rows = df.index.to_list()
        assert expected_rows == output_rows


class TestUserVOther:
    def test_returns_data_frame(self, user_stats, other_stats):
        result = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it("Df has passed user and other names as column names")
    def test_data_frame_has_expected_col_names(self, user_stats, other_stats):
        df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
        expected_cols = ["Mazza", "Cazza"]
        assert expected_cols == df.columns.to_list()

    @pytest.mark.it("Df has metrics available for both users (only) as indices")
    def test_data_frame_has_expected_row_names(self, user_stats, other_stats):
        df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
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
            "puzzles_best_rating",
        ]
        output_rows = df.index.to_list()
        assert set(expected_rows) == set(output_rows)

    @pytest.mark.it("Df populates rows with expected data from passed dictionaries")
    def test_row_data(self, user_stats, other_stats):
        df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
        expected_values = {
            "puzzles_best_rating": [2593, 1808],
            "daily_best": [1584, 1278],
            "rapid_wins": [72, 2111],
        }
        for k, v in expected_values.items():
            assert df.loc[k].tolist() == v
