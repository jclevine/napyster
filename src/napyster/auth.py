import webbrowser
from uuid import UUID
from src.common import mockable_input as input
import json
import requests


BASE_AUTH_URL = 'https://api.napster.com/oauth'
AUTHORIZE_URL = (
    '{}/authorize?client_id={{}}&redirect_uri={{}}&response_type=code&state={{}}'.format(BASE_AUTH_URL)
)

ACCESS_TOKEN_URL = '{}/access_token'.format(BASE_AUTH_URL)


def _get_temp_code(api_key, redirect_uri, state):
    webbrowser.open_new_tab(AUTHORIZE_URL.format(api_key, redirect_uri, state))
    code = input('What is the code? ')
    user_state = UUID(input('What was the state? '))

    if user_state != state:
        raise ValueError('The user state was incorrect: {} != {}'.format(user_state, state))
    return code


def get_access_token(api_key, api_secret, state, redirect_uri='localhost'):
    code = _get_temp_code(api_key, redirect_uri, state)
    data = {
        'client_id': api_key,
        'client_secret': api_secret,
        'response_type': 'code',
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    return json.loads(requests.post(ACCESS_TOKEN_URL, data=data).text)


def refresh_api_token(api_key, api_secret, refresh_token, redirect_uri='localhost'):
    data = {
        'client_id': api_key,
        'client_secret': api_secret,
        'response_type': 'code',
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'redirect_uri': redirect_uri
    }
    return json.loads(requests.post(ACCESS_TOKEN_URL, data=data).text)
