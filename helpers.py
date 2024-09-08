import requests
import polars


def get_stats(username: str) -> dict | None:
    '''
    '''
    headers = {'user-agent': 'chess-comparator'}
    
    url = f'https://api.chess.com/pub/player/{username}/stats'

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def get_profile(username: str) -> dict | None:
    '''
    '''
    headers = {'user-agent': 'chess-comparator'}
    
    url = f'https://api.chess.com/pub/player/{username}'

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None


def dict_to_df():
    pass
