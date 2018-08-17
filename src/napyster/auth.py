import webbrowser
from os import environ

from uuid import UUID, uuid4
from src.common import mockable_input as input, get_line_from_filepath as get_token_from_filepath, \
    write_line_to_filepath as write_token_to_filepath
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


def _get_new_access_tokens(api_key, api_secret, state, redirect_uri='localhost'):
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


def _refresh_api_token(api_key, api_secret, refresh_token, redirect_uri='localhost'):
    data = {
        'client_id': api_key,
        'client_secret': api_secret,
        'response_type': 'code',
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'redirect_uri': redirect_uri
    }
    return json.loads(requests.post(ACCESS_TOKEN_URL, data=data).text)


def _get_cached_tokens(last_token_path='.last_token', refresh_token_path='.refresh_token'):
    return {
        'access_token': get_token_from_filepath(last_token_path),
        'refresh_token': get_token_from_filepath(refresh_token_path)
    }


def get_access_token(last_token_path='.last_token', refresh_token_path='.refresh_token'):
    api_elements = {
        'api_key': environ['API_KEY'],
        'api_secret': environ.get('API_SECRET'),
    }
    tokens = _get_cached_tokens(last_token_path, refresh_token_path)

    if tokens['access_token'] and tokens['refresh_token']:
        pass  # Nothing. If we had both tokens, we don't need to do anything.
    elif not tokens['access_token'] and tokens['refresh_token']:
        tokens = _refresh_api_token(refresh_token=tokens['refresh_token'], **api_elements)
        write_token_to_filepath('.last_token', tokens['access_token'])
    else:
        kwargs = dict({'state': uuid4()}, **api_elements)
        tokens = _get_new_access_tokens(**kwargs)
        write_token_to_filepath('.last_token', tokens['access_token'])
        write_token_to_filepath('.refresh_token', tokens['refresh_token'])

    return tokens['access_token']
