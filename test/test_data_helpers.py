import pytest
import pandas as pd
from json import load
from data_helpers import get_current_v_best


@pytest.fixture()
def profile():
    with open("test/test_data/test_profile.json", "r") as file:
        profile = load(file)
    return profile


@pytest.fixture()
def stats():
    with open("test/test_data/test_stats.json", "r") as file:
        stats = load(file)
    return stats


class TestCurrentVBest:
    def test_returns_data_frame(self, stats):
        result = get_current_v_best(stats)
        assert isinstance(result, pd.DataFrame)

    def test_data_frame_has_expected_cols(self, stats):
        df = get_current_v_best(stats)
        expected_cols = [
            "chess_daily",
            "chess960_daily",
            "chess_rapid",
            "chess_bullet",
            "chess_blitz",
        ]
        output_cols = df.columns.to_list()
        assert expected_cols == output_cols
