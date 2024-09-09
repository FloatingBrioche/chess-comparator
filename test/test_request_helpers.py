import pytest
from request_helpers import get_profile as gp, get_stats as gs
from unittest.mock import patch
from requests.exceptions import RequestException


class TestGetProfile:
    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = gp("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = gp("Aporztian")
        assert result is None


class TestGetStats:
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
