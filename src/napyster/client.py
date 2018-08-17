from enum import Enum
from urllib.parse import urlencode
import requests
import json
from src.napyster import SimpleTrackNapster


class NapsterClient:
    class ApiVersion(Enum):
        V2_2 = '/v2.2'

        def __repr__(self):
            return self.value

        def __str__(self):
            return self.__repr__()

    BASE_URL = 'http://api.napster.com{api_version}'
    SEARCH_URL = '{}{}'.format(BASE_URL, '/search')
    SEARCH_VERBOSE_URL = '{}{}'.format(SEARCH_URL, '/verbose')

    def __init__(self, api_key, access_token_provider):
        self._api_key = api_key
        self._access_token_provider = access_token_provider

    def search_for_track_by_album(self, query_track, api_version=ApiVersion.V2_2):
        query = '{} {}'.format(query_track.artist_name, query_track.title)
        query_params = urlencode({
            'apikey': self._api_key,
            'query': query,
            'type': 'track'
        })
        url = self.SEARCH_VERBOSE_URL.format(api_version=api_version)
        headers = {'Authorization': 'Bearer {}'.format(self._access_token_provider())}
        response = json.loads(requests.get(url, query_params, headers=headers).text)
        tracks = {
            SimpleTrackNapster(track)
            for track
            in response['search']['data']['tracks']
            if query_track.album_title in track['albumName'] and query_track.artist_name == track['artistName']
        }
        return tracks
