import pytest
from request_helpers import get_profile as gp, get_stats as gs
from unittest.mock import patch, Mock
from requests.exceptions import RequestException


@pytest.fixture
def mock_response():
    mock_response = Mock()
    mock_response.status_code = 500
    return mock_response


class TestGetProfile:
    @pytest.mark.it("Uses username parameter in get request")
    @patch("request_helpers.api_get")
    def test_get_request(self, mock_api_get, mock_response):
        mock_api_get.return_value = mock_response
        gp("Aporztian")
        mock_api_get.assert_called_once_with(
            "https://api.chess.com/pub/player/Aporztian",
            headers={"user-agent": "chess-comparator"},
        )

    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = gp("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = gp("Aporztian")
        assert result is None


class TestGetStats:
    @pytest.mark.it("Uses username parameter in get request")
    @patch("request_helpers.api_get")
    def test_get_request(self, mock_api_get, mock_response):
        mock_api_get.return_value = mock_response
        gs("Aporztian")
        mock_api_get.assert_called_once_with(
            "https://api.chess.com/pub/player/Aporztian/stats",
            headers={"user-agent": "chess-comparator"},
        )

    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = gs("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = gs("Aporztian")
        assert result is None


class TestLogging:
    @patch("request_helpers.api_get", side_effect=RequestException("Test exception"))
    def test_get_profile_logging(self, mock_api_get, caplog):
        gp("Aporian")
        assert "Request error" in caplog.text

    @patch("request_helpers.api_get", side_effect=RequestException("Test exception"))
    def test_get_stats_logging(self, mock_api_get, caplog):
        gs("Aporian")
        assert "Request error" in caplog.text
