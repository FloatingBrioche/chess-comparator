from unittest.mock import patch, Mock, AsyncMock
import time
import sys

import pytest
import httpx
from requests.exceptions import RequestException

from helpers.vars import required_game_archive_keys

# to remove unpatched module if already imported
sys.modules.pop("helpers.request_helpers", None) 


def mock_streamlit_cache_data(func):
    """
    Mock of the st.cache_data decorator for testing purposes.
    """

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

# patch the st.cache_data decorator before the functions are defined
st_cache_patcher = patch("streamlit.cache_data", mock_streamlit_cache_data)

st_cache_patcher.start()

from helpers.request_helpers import (
    get_profile,
    get_stats,
    get_gms,
    get_puzzle,
    get_compatriots,
    get_random_gm,
    get_random_compatriot,
    get_archives,
    get_archive,
    get_game_history,
    return_game_history,
)

### Fixtures ###


@pytest.fixture
def mock_response():
    mock_response = Mock()
    mock_response.status_code = 500
    return mock_response


### Tests ###


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

    @pytest.mark.it("Returns list when passed valid username")
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
    @pytest.mark.asyncio(loop_scope="function")
    async def test_uses_username_param(self, mock_response):
        client = AsyncMock()
        client.get.return_value = mock_response
        url = "egg"
        result = await get_archive(url, client)
        client.get.assert_called_once_with(
            "egg", headers={"user-agent": "chess-comparator"}
        )

    @pytest.mark.it("Returns list for valid url")
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_list(self):
        async with httpx.AsyncClient() as client:
            url = "https://api.chess.com/pub/player/aporian/games/2008/12"
            output = await get_archive(url, client)
        assert isinstance(output, list)

    @pytest.mark.it("Returns none for invalid url/404 reponse")
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_none_404(self):
        async with httpx.AsyncClient() as client:
            url = "https://api.chess.com/pub/player/aporian/games/2008/123"
            output = await get_archive(url, client)
        assert output is None

    @pytest.mark.it("Returns none for 500 reponse")
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_none_500(self, mock_response):
        url = "https://api.chess.com/pub/player/aporian/games/2008/12"
        client = AsyncMock()
        client.get.return_value = mock_response
        output = await get_archive(url, client)
        assert output is None

    @pytest.mark.it("Logs request exceptions")
    @pytest.mark.asyncio(loop_scope="function")
    async def test_logs_request_exceptions(self, caplog):
        client = AsyncMock()
        client.get.side_effect = httpx.RequestError("Request error")
        url = "egg"
        result = await get_archive(url, client)
        assert "Request error" in caplog.text

    @pytest.mark.skip(
        "Skipping tests to avoid nigh number of API calls. Tests passing as of 12-05-25"
    )
    class TestGetGameHistory:
        @pytest.mark.it("Returns list of dictionaries")
        @pytest.mark.asyncio(loop_scope="function")
        async def test_returns_None(self):
            result = await get_game_history("Aporian")
            assert isinstance(result, list)
            assert all(isinstance(game, dict) for game in result)

        @pytest.mark.it("each dict (game archive) has required keys")
        @pytest.mark.asyncio(loop_scope="function")
        async def test_game_archive_dicts_have_required_keys(self):
            game_history = await get_game_history("Aporian")
            for game in game_history:
                game_keys = set(game.keys())
                assert all([key in game_keys for key in required_game_archive_keys])

        @pytest.mark.it("Executes in <2 seconds for large set of archives")
        @pytest.mark.asyncio(loop_scope="function")
        async def test_performant_execution(self):
            start = time.time()
            game_history = await get_game_history("Aporian")
            end = time.time()
            execution_time = end - start
            print(f"Execution time = {execution_time:.2f}")
            print(f"Number of requests = {len(game_history)}")
            assert execution_time < 2


st_cache_patcher.stop()
