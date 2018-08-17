from unittest import TestCase
from src.napyster import SimpleTrackNapster as Track
from src.napyster import NapsterClient
from unittest.mock import patch, Mock
from src.napyster import SimpleTrackNapster
from tests.common import mock_single_search_answer_response


class TestClient(TestCase):

    @patch('src.napyster.client.requests.get', return_value=mock_single_search_answer_response())
    def test_when_search_for_song_then_you_get_track(self, mock_get):
        """
        Given Atlas Sound||Logos||Quick Canal returns only one result
         When you search for the track Atlas Sound||Logos||Quick Canal
         Then you get that track
        """
        client = NapsterClient('api-key', Mock(return_value='access-token'))
        simple_track = SimpleTrackNapster.build('Atlas Sound', 'Logos', 'Quick Canal')
        actual = client.search_for_track_by_album(simple_track)
        self.assertEqual(simple_track, actual)
        expected_url = 'http://api.napster.com/v2.2/search/verbose'
        expected_query_params = 'apikey=api-key&query=Atlas+Sound+Quick+Canal&type=track'
        expected_headers = {'Authorization': 'Bearer access-token'}
        mock_get.assert_called_with(expected_url, expected_query_params, headers=expected_headers)
