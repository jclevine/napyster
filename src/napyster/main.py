from os import environ
from src.napyster import get_access_token, refresh_api_token
from uuid import uuid4
from src.common import get_line_from_filepath as get_token_from_filepath
from src.common import write_line_to_filepath as write_token_to_filepath


def get_cached_tokens(last_token_path='.last_token', refresh_token_path='.refresh_token'):
    return {
        'access_token': get_token_from_filepath(last_token_path),
        'refresh_token': get_token_from_filepath(refresh_token_path)
    }


def main(last_token_path='.last_token', refresh_token_path='.refresh_token'):
    api_elements = {
        'api_key': environ['API_KEY'],
        'api_secret': environ.get('API_SECRET'),
    }
    tokens = get_cached_tokens(last_token_path, refresh_token_path)

    if tokens['access_token'] and tokens['refresh_token']:
        pass  # Nothing. If we had both tokens, we don't need to do anything.
    elif not tokens['access_token'] and tokens['refresh_token']:
        tokens = refresh_api_token(refresh_token=tokens['refresh_token'], **api_elements)
        write_token_to_filepath('.last_token', tokens['access_token'])
    else:
        kwargs = dict({'state': uuid4()}, **api_elements)
        tokens = get_access_token(**kwargs)
        write_token_to_filepath('.last_token', tokens['access_token'])
        write_token_to_filepath('.refresh_token', tokens['refresh_token'])

    return tokens


if __name__ == '__main__':  # pragma: no cover
    main()
