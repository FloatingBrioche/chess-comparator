import pytest
import pandas as pd
from unittest.mock import patch
from json import load
from helpers.classes import ChessUser


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
@patch("helpers.classes.get_profile")
def TestAporian(mock_get_profile, profile):
    mock_get_profile.return_value = profile
    return ChessUser("Aporian")


@pytest.fixture(scope="function")
@patch("helpers.classes.get_stats")
@patch("helpers.classes.get_profile")
def TestAporianStatsAdded(mock_get_profile, mock_get_stats, profile, aporian_stats):
    mock_get_profile.return_value = profile
    mock_get_stats.return_value = aporian_stats
    TestAporianStatsAdded = ChessUser("Aporian")
    TestAporianStatsAdded.add_stats()
    return TestAporianStatsAdded


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
    @patch("helpers.classes.get_stats")
    def test_updates_profile_name(self, mock_get_stats, TestAporian):
        TestAporian.add_stats()
        assert TestAporian.name == "Martin C."

    @pytest.mark.it("Updates name att to username if profile doesn't contain name")
    @patch("helpers.classes.get_stats")
    @patch("helpers.classes.get_profile")
    def test_updates_name_username(self, mock_get_profile, mock_get_stats, profile):
        del profile["name"]
        mock_get_profile.return_value = profile
        TestAporianNoName = ChessUser("Aporian")
        TestAporianNoName.add_stats()
        assert TestAporianNoName.name == "Aporian"

    @pytest.mark.it("Updates stats attribute with dictionary")
    @patch("helpers.classes.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.stats is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.stats, dict)

    @pytest.mark.it("Updates country attribute with country code string")
    @patch("helpers.classes.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.country is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.country, str)
        assert TestAporian.country == "XE"

    @pytest.mark.it("Updates available_metrics attribute with set")
    @patch("helpers.classes.get_stats")
    def test_updates_stats(self, mock_get_stats, TestAporian, aporian_stats):
        mock_get_stats.return_value = aporian_stats
        assert TestAporian.available_metrics is None
        TestAporian.add_stats()
        assert isinstance(TestAporian.available_metrics, set)

    @pytest.mark.it("Available_metrics is set of stats keys")
    @patch("helpers.classes.get_stats")
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
