import pytest
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from helpers.plot_helpers import plot_pie
from helpers.vars import totals_indices


@pytest.fixture()
def expanded_df():
    expanded_df = pd.read_csv("test/test_data/expanded_u_vs_oth_df.csv", index_col=0)
    return expanded_df


class TestPlotPie:
    def test_returns_plottable_object(self, expanded_df):
        output = plot_pie(expanded_df, "Mazza", totals_indices)
        assert isinstance(output, Figure)

    def test_takes_passed_name_as_y_label(self, expanded_df):
        output = plot_pie(expanded_df, "Cazza", totals_indices)
        assert output.get_axes()[0].get_ylabel() == "Cazza"