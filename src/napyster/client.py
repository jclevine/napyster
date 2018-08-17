from enum import Enum
from urllib.parse import urlencode
import requests
import json
from src.napyster import SimpleTrackNapster
from ngram import NGram


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
    ME_URL = '{}{}'.format(BASE_URL, '/me')
    FAVOURITES_URL = '{}{}'.format(ME_URL, '/favorites')

    def __init__(self, api_key, access_token_provider):
        self._api_key = api_key
        self._access_token_provider = access_token_provider

    def search_for_track_by_album(self, query_track, api_version=ApiVersion.V2_2):
        perms = self.get_search_permutations(query_track)

        for query in perms:
            # query = '{} {}'.format(query_track.artist_name, query_track.title)
            query_params = urlencode({
                'apikey': self._api_key,
                'query': query,
                'type': 'track'
            })
            url = self.SEARCH_VERBOSE_URL.format(api_version=api_version)
            headers = {'Authorization': 'Bearer {}'.format(self._access_token_provider())}
            response = json.loads(requests.get(url, query_params, headers=headers).text)
            simple_tracks = {
                SimpleTrackNapster(track)
                for track
                in response['search']['data']['tracks']
            }

            final_track = {
                track for track in simple_tracks
                if (
                       (
                           NGram.compare(query_track.album_title, track.album_title, N=1) > 0.8 or
                           query_track.album_title in track.album_title
                        ) and
                       query_track.artist_name == track.artist_name and
                       query_track.title in track.title

                )
            }

            if len(final_track) > 0:
                return final_track
        return {}

    @staticmethod
    def get_search_permutations(query_track):
        perms = []
        for (artistNameThe, trackNameThe) in [(' ', ' '), ('the ', ' '), (' ', ' the '), ('the ', ' the ')]:
            perms.append('{}{}{}{}'.format(
                artistNameThe, query_track.artist_name, trackNameThe, query_track.title).strip())
        return perms

    def mark_tracks_as_favourite(self, tracks, api_version=ApiVersion.V2_2):
        url = self.FAVOURITES_URL.format(api_version=api_version)
        headers = {
            'Authorization': 'Bearer {}'.format(self._access_token_provider()),
            'Content-Type': 'application/json'
        }
        data = {
            'favorites': [
                {'id': track.id} for track in tracks
            ]
        }
        return json.loads(requests.post(url, headers=headers, data=json.dumps(data)).text)
