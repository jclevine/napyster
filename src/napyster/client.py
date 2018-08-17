from enum import Enum
from urllib.parse import urlencode
import requests
import json


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

    def __init__(self, api_key):
        self._api_key = api_key

    def search_for_track(self, query, api_version=ApiVersion.V2_2):
        query_params = urlencode({
            'apikey': self._api_key,
            'query': 'Weezer My Name Is Jonas',
            'type': 'track'
        })
        url = self.SEARCH_VERBOSE_URL.format(api_version=api_version)
        response = json.loads(requests.get(url, query_params).text)
        # response = json.loads(requests.get(url).text)
        print(response)
