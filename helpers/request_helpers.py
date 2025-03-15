from requests import get as get_request
from requests.exceptions import RequestException
from httpx import RequestError
from os.path import isfile
from json import load, dump
from random import choice
from helpers.loggers import request_logger
from helpers.vars import old_puzzle


headers = {"user-agent": "chess-comparator"}


def get_profile(username: str) -> dict | None:
    """
    Retrieves Chess.com profile via API using username.

    Takes a string and uses the requests library to call the Chess.com API
    and retrieve the profile data for the given username.

    If the string is a valid username, i.e. if the request receives a
    200 response, the JSON is converted to a dictionary and returned.
    If not, returns None.

    Parameters:
        - username: str, should match a chess.com username.

    Returns:
        - A dictionary of chess.com profile data (for a 200 response)
            OR
        - None (for any other response)"""

    try:
        url = f"https://api.chess.com/pub/player/{username}"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except RequestException as e:
        request_logger.error(f"Request error: {e}")


def get_stats(username: str) -> dict | None:
    """
    Retrieves Chess.com stats via API using username.

    Takes a username string and uses the requests library
    to call the Chess.com API and retrieve user stats
    for the given user.

    If the string is a valid username, i.e. if the request
    receives a 200 response, the JSON is converted to a dictionary
    and returned. If not, returns None.

    Parameters:
        - username [str]: should match a chess.com username.

    Returns:
        - A dictionary of Chess.com profile data (for a 200 response)
            OR
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
        request_logger.error(f"Request error: {repr(e)}")


def get_gms() -> list:
    """
    Returns a list of Chess.coms GMs retrieved via API.

    Uses the requests library to call the Chess.com API
    and retrieve JSON data of the GMs who use the site.

    If the request receives a 200 response,
    the JSON is converted to a list and returned.
    If not, returns None.

    Args:
        - N/A

    Returns:
        - A list of chess.com GMs (for a 200 response)
            OR
        - None (for any other response)
    """
    try:
        url = "https://api.chess.com/pub/titled/GM"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()["players"]
        else:
            return None

    except RequestException as e:
        request_logger.error(f"Request error: {e}")


def get_compatriots(iso: str):
    """
    Returns a list of Chess.coms users retrieve via API.

    Uses the requests library to call the Chess.com API
    and retrieve JSON data of the users from a particular country.
    If the request receives a 200 response,
    the JSON is converted to a list and returned. If not, returns None.

    Args:
        - iso [str]: a string of the a country's ISO code

    Returns:
        - A list of chess.com users (for a 200 response)
            OR
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
        request_logger.error(f"Request error: {e}")


def get_random_gm() -> str:
    """
    Returns the username of a randomly chosen GM.

    Checks if JSON of GMs is stored. If so, loads
    the list and uses the random library to chose and
    return a GM from the list.

    If no JSON data is currently stored, calls the get_gms
    function to retrieve the list via API and save it before
    selecting the GM.

    Args:
        - N/A

    Returns:
        -  a string of the username of a GM

    Raises:
        - N/A
    """

    if isfile("./storage/saved_gms.json"):
        with open("./storage/saved_gms.json", "r") as jsizzle:
            gms = load(jsizzle)
    else:
        gms = get_gms()
        with open("./storage/saved_gms.json", "w") as jsizzle:
            dump(gms, jsizzle)
    return choice(gms)


def get_random_compatriot(iso: str):
    """
    Returns the username of a random user from the same country.

    Checks if JSON of users is stored. If so, loads
    the list and uses the random library to chose and
    return a user from the list.

    If no JSON data is currently stored, calls the get_compatriots
    function to retrieve the list via API and save it before
    selecting the user.

    Args:
        - iso [str]: a string of the a country's ISO code

    Returns:
        -  string of the username of a user

    Raises:
        - N/A
    """
    if isfile(f"./storage/{iso}.json"):
        with open(f"./storage/{iso}.json", "r") as jsizzle:
            compatriots = load(jsizzle)
    else:
        compatriots = get_compatriots(iso)
        with open(f"./storage/{iso}.json", "w") as jsizzle:
            dump(compatriots, jsizzle)
    return choice(compatriots)


def get_puzzle():
    """
    Returns Chess.com puzzle.

    Uses the requests library to call the Chess.com API and retrieve
    JSON for a chess puzzle.

    If the request receives a 200 response, the JSON is converted
    to a dictionary and returned. If not, returns an old puzzle.

    Args:
        - N/A

    Returns:
        - A dictionary of the current Chess.com daily puzzle
            (for a 200 response)
            OR
        - A dictionary of an old Chess.com daily puzzle
            (for any other response)
    """

    try:
        url = "https://api.chess.com/pub/puzzle"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return old_puzzle

    except RequestException as e:
        request_logger.error(f"Request error: {e}")


def get_archives(username: str) -> list | None:
    """
    Returns list of Chess.com monthly archives.

    Takes a username string and uses the requests library
    to call the Chess.com API and retrieve monthly archives
    for the given user.

    If the request receives a 200 response, the JSON is converted
    to a list and returned. If not, returns None.

    Args:
        - username [str]: string of username

    Returns:
        - A list of the monthly Chess.com archives
            (for a 200 response)
            OR
        - None
            (for any other response)
    """

    try:
        url = f"https://api.chess.com/pub/player/{username}/games/archives"

        response = get_request(url, headers=headers)

        if response.status_code == 200:
            return response.json()["archives"]
        else:
            return None

    except RequestException as e:
        request_logger.error(f"Request error: {e}")


async def get_archive(url, client):
    """
    Returns list of Chess.com games for given month.

    Takes a url string and a httpx.AsyncClient object and uses the httpx library
    to call the Chess.com API and retrieve that month's games
    for the given user.

    If the request receives a 200 response, the JSON is converted
    to a list and returned. If not, returns None.

    Args:
        - url [str]: a string of a monthly archive url
        - client: a httpx.AsyncClient object passed in from the enclosing function

    Returns:
        - A list of the Chess.com games archives for the url
            (for a 200 response)
            OR
        - None
            (for any other response)
    """

    try:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()["games"]
        else:
            return None

    except RequestError as e:
        request_logger.error(f"Request error: {str(e)}, url = {url}")
