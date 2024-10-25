import pytest
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from helpers.plot_helpers import plot_pie
from helpers.vars import indices


@pytest.fixture()
def expanded_df():
    expanded_df = pd.read_csv("test/test_data/test_df.csv", index_col=0)
    return expanded_df


class TestPlotPie:
    def test_returns_plottable_object(self, expanded_df):
        output = plot_pie(expanded_df, "Mazza", indices['totals'])
        assert isinstance(output, Figure)

    def test_takes_passed_name_as_y_label(self, expanded_df):
        output = plot_pie(expanded_df, "Cazza", indices['totals'])
        assert output.get_axes()[0].get_ylabel() == "Cazza"