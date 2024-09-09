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

    @pytest.mark.it("Df has 'current' and 'best' as column names")
    def test_data_frame_has_expected_col_names(self, stats):
        df = get_current_v_best(stats)
        expected_cols = [
            "current",
            "best"   
        ]
        output_cols = df.columns.to_list()
        assert expected_cols == output_cols
    
    @pytest.mark.it("Df has game types as indices")
    def test_data_frame_has_expected_row_names(self, stats):
        df = get_current_v_best(stats)
        expected_rows = [
            "daily",
            "chess960_daily",
            "rapid",
            "bullet",
            "blitz"
        ]
        output_rows = df.index.to_list()
        assert expected_rows == output_rows
