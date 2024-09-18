from requests import get as get_request
from requests.exceptions import RequestException
from os.path import isfile
from json import load, dump
from random import choice
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


def get_compatriots(iso: str):
    """
    Uses the requests library to call the Chess.com API
    and retrieve JSON data of the users from a particular country.

    If the request receives a 200 response,
    the JSON is converted to a list and returned. If not, returns None.

    Parameters:
    - iso: str

    Returns either:
    - A list of chess.com users (for a 200 response)
    - None (for any other response)
    """
    try:
        url = f"https://api.chess.com/pub/country/{iso}/players"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()["players"]
        else:
            return None

    except RequestException as e:
        logger.error(f"Request error: {e}")    


def get_random_gm():
    if isfile("./storage/saved_gms.json"):
        with open("./storage/saved_gms.json", "r") as jsizzle:
            gms = load(jsizzle)
    else:
        gms = get_gms()
        with open("./storage/saved_gms.json", "w") as jsizzle:
            dump(gms, jsizzle)
    return choice(gms)


def get_random_compatriot(iso):
    if isfile(f'./storage/{iso}.json'):
        with open(f"./storage/{iso}.json", "r") as jsizzle:
            compatriots = load(jsizzle)
    else:
        compatriots = get_compatriots(iso)
        with open(f"./storage/{iso}.json", "w") as jsizzle:
            dump(compatriots, jsizzle)
    return choice(compatriots)