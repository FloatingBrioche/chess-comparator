import pytest
import pandas as pd
from json import load
from helpers.classes import ChessUser, Comparison


# class TestUserVOther:
#     def test_returns_data_frame(self, user_stats, other_stats):
#         result = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
#         assert isinstance(result, pd.DataFrame)

#     @pytest.mark.it("Df has passed user and other names as column names")
#     def test_data_frame_has_expected_col_names(self, user_stats, other_stats):
#         df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
#         expected_cols = ["Mazza", "Cazza"]
#         assert expected_cols == df.columns.to_list()

#     @pytest.mark.it("Df has metrics available for both users (only) as indices")
#     def test_data_frame_has_expected_row_names(self, user_stats, other_stats):
#         df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
#         expected_rows = [
#             "blitz_best",
#             "blitz_current",
#             "blitz_wins",
#             "blitz_draws",
#             "blitz_losses",
#             "daily_best",
#             "daily_current",
#             "daily_wins",
#             "daily_draws",
#             "daily_losses",
#             "rapid_best",
#             "rapid_current",
#             "rapid_wins",
#             "rapid_draws",
#             "rapid_losses",
#             "puzzle_rush",
#             "puzzles",
#         ]
#         output_rows = df.index.to_list()
#         assert set(expected_rows) == set(output_rows)

#     @pytest.mark.it("Df populates rows with expected data from passed dicts")
#     def test_row_data(self, user_stats, other_stats):
#         df = get_user_v_other({"Mazza": user_stats}, {"Cazza": other_stats})
#         expected_values = {
#             "puzzles": [2593, 1808],
#             "daily_best": [1584, 1278],
#             "rapid_wins": [72, 2111],
#         }
#         for k, v in expected_values.items():
#             assert df.loc[k].tolist() == v


# class TestExpandData:
#     def test_returns_data_frame(self, u_vs_oth_df):
#         output = expand_data(u_vs_oth_df)
#         assert isinstance(output, pd.DataFrame)

#     def test_new_df_has_total_games_index(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         assert "total_games" in df.index.to_list()

#     def test_new_df_has_total_wins_draws_losses_indices(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         indices = df.index.to_list()
#         assert "total_wins" in indices
#         assert "total_draws" in indices
#         assert "total_losses" in indices

#     def test_calculates_total_wins(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         expected = [3, 3]
#         actual = df.loc["total_wins"].to_list()
#         assert actual == expected

#     def test_calculates_total_draws(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         expected = [3, 3]
#         actual = df.loc["total_draws"].to_list()
#         assert actual == expected

#     def test_calculates_total_losses(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         expected = [3, 3]
#         actual = df.loc["total_losses"].to_list()
#         assert actual == expected

#     def test_calculates_total_games(self, u_vs_oth_df):
#         df = expand_data(u_vs_oth_df)
#         expected = [9, 9]
#         actual = df.loc["total_games"].to_list()
#         assert actual == expected


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