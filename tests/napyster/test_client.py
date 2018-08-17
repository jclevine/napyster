from unittest import TestCase
from src.napyster import SimpleTrackNapster as Track
from src.napyster import NapsterClient
from os import environ
from unittest.mock import patch
import os


@patch.dict(os.environ, {'API_KEY': 'api-key', 'API_SECRET': 'secret'})
class TestClient(TestCase):

    def test_when_search_for_song_then_you_get_track(self):
        """
         When you search for the song My Name Is Jonas by Weezer
         Then you get that track
        """
        api_key = environ['API_KEY']
        client = NapsterClient(api_key)
        track = client.search_for_track('Weezer Weezer My Name Is Jonas')
        self.assertEqual(track, Track.build('Weezer', 'Weezer', 'My Name Is Jonas'))

        """
        curl -v -X POST  -H "Authorization: Bearer {access_token}" -H "Content-Type: application/json"
        -d '{"favorites": [ {"id":"alb.54719066"}, {"id":"tra.54719072"} ]}'
        "https://api.napster.com/v2.2/me/favorites"

        """
