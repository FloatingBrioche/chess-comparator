import pytest
import httpx
from unittest.mock import patch, Mock, AsyncMock
from requests.exceptions import RequestException
from helpers.request_helpers import (
    get_profile,
    get_stats,
    get_gms,
    get_puzzle,
    get_compatriots,
    get_random_gm,
    get_random_compatriot,
    get_archives,
    get_archive
)



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

    @patch(
        "helpers.request_helpers.get_request",
        side_effect=RequestException("Test exception"),
    )
    def test_logs_get_profile_request_exceptions(self, mock_api_get, caplog):
        get_profile("Aporian")
        assert "Request error" in caplog.text


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

    @patch(
        "helpers.request_helpers.get_request",
        side_effect=RequestException("Test exception"),
    )
    def test_logs_get_stats_request_exceptions(self, mock_api_get, caplog):
        get_stats("Aporian")
        assert "Request error" in caplog.text


class TestGetGMs:
    def test_returns_list(self):
        output = get_gms()
        assert isinstance(output, list)

    def test_list_has_expects_gms(self):
        expected_gms = ["magnuscarlsen", "hikaru", "firouzja2003"]
        output = get_gms()
        assert all(gm in output for gm in expected_gms)

    @patch(
        "helpers.request_helpers.get_request",
        side_effect=RequestException("Test exception"),
    )
    def test_logs_get_gms_request_exceptions(self, mock_api_get, caplog):
        get_gms()
        assert "Request error" in caplog.text


class TestGetPuzzle:
    def test_returns_dict(self):
        output = get_puzzle()
        print(output)
        assert isinstance(output, dict)

    @patch(
        "helpers.request_helpers.get_request",
        side_effect=RequestException("Test exception"),
    )
    def test_logs_get_puzzle_request_exceptions(self, mock_api_get, caplog):
        get_puzzle()
        assert "Request error" in caplog.text


class TestGetArchives:
    @pytest.mark.it("Uses username parameter in get request")
    @patch("helpers.request_helpers.get_request")
    def test_uses_username_param(self, mock_api_get, mock_response):
        mock_api_get.return_value = mock_response
        get_archives("Aporztian")
        mock_api_get.assert_called_once_with(
            "https://api.chess.com/pub/player/Aporztian/games/archives",
            headers={"user-agent": "chess-comparator"},
        )
    
    @pytest.mark.it("Returns list")
    def test_returns_list(self):
        output = get_archives("Aporian")
        assert isinstance(output, list)

    @pytest.mark.it("Logs request exceptions")
    @patch(
        "helpers.request_helpers.get_request",
        side_effect=RequestException("Test exception"),
    )
    def test_logs_request_exceptions(self, mock_api_get, caplog):
        get_archives("Aporian")
        assert "Request error" in caplog.text


class TestGetArchive:
    @pytest.mark.it("Uses url parameter in get request")
    @pytest.mark.asyncio(loop_scope='function')
    async def test_uses_username_param(self, mock_response):
        client = AsyncMock()
        client.get.return_value=mock_response
        url = "egg"
        result = await get_archive(url, client)
        client.get.assert_called_once_with('egg', headers={'user-agent': 'chess-comparator'})

    
    # @pytest.mark.it("Returns list")
    # @pytest.mark.asyncio(loop_scope='function')
    # async def test_returns_list(self):
    #     async with httpx.AsyncClient() as client:
    #         url = "https://api.chess.com/pub/player/Aporztian/games/2020/12"
    #         output = await get_archive(url, client)
    #     assert isinstance(output, list)

    # @pytest.mark.it("Logs request exceptions")
    # @patch(
    #     "helpers.request_helpers.get_request",
    #     side_effect=httpx.RequestError("Test exception"),
    # )
    # def test_logs_request_exceptions(self, mock_api_get, caplog):
    #                 url = "https://api.chess.com/pub/player/Aporztian/games/2020/12"
    #     get_archive("Aporztian", 2020, 12)
    #     assert "Request error" in caplog.text






