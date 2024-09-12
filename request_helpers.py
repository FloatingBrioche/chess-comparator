from requests import get as get_request
from requests.exceptions import RequestException
import logging


logging.basicConfig(
    filename="logs/request-errors.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S"
)

logger = logging.getLogger()


headers = {"user-agent": "chess-comparator"}


def get_profile(username: str) -> dict | None:
    """
    Takes a string and uses the requests library to call the Chess.com API
    and retrieve profile data for the profile with that string as the username.

    If the string is a valid username, i.e. if the request receives a 200 response,
    the JSON is converted to a dictionary and returned. If not, returns None.

    Parameters:
    - username: str, should match a chess.com username.

    Returns either:
    - A dictionary of chess.com profile data (for a 200 response)
    - None (for any other response)"""

    try:
        url = f"https://api.chess.com/pub/player/{username}"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except RequestException as e:
        logger.error(f"Request error: {e}")


def get_stats(username: str) -> dict | None:
    """
    Takes a string and uses the requests library to call the Chess.com API
    and retrieve user stats for the user with that string as the username.

    If the string is a valid username, i.e. if the request receives a 200 response,
    the JSON is converted to a dictionary and returned. If not, returns None.

    Parameters:
    - username: str, should match a chess.com username.

    Returns either:
    - A dictionary of chess.com profile data (for a 200 response)
    - None (for any other response)
    """
    try:
        url = f"https://api.chess.com/pub/player/{username}/stats"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except RequestException as e:
        logger.error(f"Request error: {e}")


def get_gms() -> list:
    """
    Uses the requests library to call the Chess.com API
    and retrieve JSON data of the GMs who use the site.

    If the request receives a 200 response,
    the JSON is converted to a list and returned. If not, returns None.

    Parameters:
    - none

    Returns either:
    - A list of chess.com GMs (for a 200 response)
    - None (for any other response)
    """
    try:
        url = f"https://api.chess.com/pub/titled/GM"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()["players"]
        else:
            return None

    except RequestException as e:
        logger.error(f"Request error: {e}")