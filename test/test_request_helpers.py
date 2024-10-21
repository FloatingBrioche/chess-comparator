import pytest
from helpers.request_helpers import get_profile, get_stats, get_gms, get_puzzle
from unittest.mock import patch, Mock
from requests.exceptions import RequestException


@pytest.fixture
def mock_response():
    mock_response = Mock()
    mock_response.status_code = 500
    return mock_response


class TestGetProfile:
    @pytest.mark.it("Uses username parameter in get request")
    @patch("helpers.request_helpers.get_request")
    def test_get_request(self, mock_api_get, mock_response):
        mock_api_get.return_value = mock_response
        get_profile("Aporztian")
        mock_api_get.assert_called_once_with(
            "https://api.chess.com/pub/player/Aporztian",
            headers={"user-agent": "chess-comparator"},
        )

    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = get_profile("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = get_profile("Aporztian")
        assert result is None


class TestGetStats:
    @pytest.mark.it("Uses username parameter in get request")
    @patch("helpers.request_helpers.get_request")
    def test_get_request(self, mock_api_get, mock_response):
        mock_api_get.return_value = mock_response
        get_stats("Aporztian")
        mock_api_get.assert_called_once_with(
            "https://api.chess.com/pub/player/Aporztian/stats",
            headers={"user-agent": "chess-comparator"},
        )

    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = get_stats("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = get_stats("Aporztian")
        assert result is None

class TestGetGMs:
    def test_returns_list(self):
        output = get_gms()
        assert isinstance(output, list)

    def test_list_has_expects_gms(self):
        expected_gms = ["magnuscarlsen", "hikaru", "firouzja2003"]
        output = get_gms()
        assert all(gm in output for gm in expected_gms)

class TestGetPuzzle:
    def test_returns_dict(self):
        output = get_puzzle()
        assert isinstance(output, dict)


class TestLogging:
    @patch("helpers.request_helpers.get_request", side_effect=RequestException("Test exception"))
    def test_logs_get_profile_request_exceptions(self, mock_api_get, caplog):
        get_profile("Aporian")
        assert "Request error" in caplog.text

    @patch("helpers.request_helpers.get_request", side_effect=RequestException("Test exception"))
    def test_logs_get_stats_request_exceptions(self, mock_api_get, caplog):
        get_stats("Aporian")
        assert "Request error" in caplog.text

    @patch("helpers.request_helpers.get_request", side_effect=RequestException("Test exception"))
    def test_logs_get_gms_request_exceptions(self, mock_api_get, caplog):
        get_gms()
        assert "Request error" in caplog.text

    @patch("helpers.request_helpers.get_request", side_effect=RequestException("Test exception"))
    def test_logs_get_puzzle_request_exceptions(self, mock_api_get, caplog):
        get_puzzle()
        assert "Request error" in caplog.text
