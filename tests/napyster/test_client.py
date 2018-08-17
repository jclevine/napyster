from unittest import TestCase
from src.napyster import SimpleTrackNapster as Track
from src.napyster import NapsterClient
from unittest.mock import patch, Mock
from src.napyster import SimpleTrackNapster
from tests.common import mock_single_search_answer_response


class TestClient(TestCase):

    @patch('src.napyster.client.requests.get', return_value=mock_single_search_answer_response(
        '{"search":{"data":{"tracks":[{"type":"track","id":"track-id",'
        '"name":"Quick Canal","artistName":"Atlas Sound","albumName":"Logos"}]}}}'
    ))
    def test_when_search_for_song_then_you_get_one_track(self, mock_get):
        """
        Given Atlas Sound||Logos||Quick Canal returns only one result
         When you search for the track Atlas Sound||Logos||Quick Canal
         Then you get that track
        """
        client = NapsterClient('api-key', Mock(return_value='access-token'))
        simple_track = SimpleTrackNapster.build('Atlas Sound', 'Logos', 'Quick Canal', id='track-id')
        actual = client.search_for_track_by_album(simple_track)
        self.assertSetEqual({simple_track}, actual)
        expected_url = 'http://api.napster.com/v2.2/search/verbose'
        expected_query_params = 'apikey=api-key&query=Atlas+Sound+Quick+Canal&type=track'
        expected_headers = {'Authorization': 'Bearer access-token'}
        mock_get.assert_called_with(expected_url, expected_query_params, headers=expected_headers)

    @patch('src.napyster.client.requests.get', return_value=mock_single_search_answer_response(
        '{"search":{"data":{"tracks":['
        '{"type":"track","id":"blue-id","name":"My Name Is Jonas",'
        '"artistName":"Weezer","albumName":"Weezer (Blue Album)"},'
        '{"type":"track","id":"deluxe-id","name":"My Name Is Jonas",'
        '"artistName":"Weezer","albumName":"Weezer (Blue Album) (Deluxe Edition)"},'
        '{"type":"track","id":"deluxe-bside-id","name":"My Name Is Jonas - (live, b-side)",'
        '"artistName":"Weezer","albumName":"Weezer (Blue Album) (Deluxe Edition)"},'
        '{"type":"track","id":"what","name":"My Name Is Jonas",'
        '"artistName":"Rockabye Baby!","albumName":"Rockabye Baby! Lullaby Renditions of Weezer"}'
        ']}}}'
    ))
    def test_when_search_for_song_that_is_in_multiple_albums_then_you_get_list_of_albums(self, mock_get):
        """
        Given Weezer||Weezer||My Name Is Jones returns 4 results
          and 2 are tracks from same deluxe album, 1 is original album, and 1 is some random thing
         When you search for the track Weezer||Weezer||My Name Is Jones
         Then you get a list of the possible albums
        """
        client = NapsterClient('api-key', Mock(return_value='access-token'))
        simple_track = SimpleTrackNapster.build('Weezer', 'Weezer', 'My Name Is Jonas')
        actual = client.search_for_track_by_album(simple_track)
        expected = {
            SimpleTrackNapster.build('Weezer', 'Weezer (Blue Album)', 'My Name Is Jonas', id='blue-id'),
            SimpleTrackNapster.build(
                'Weezer', 'Weezer (Blue Album) (Deluxe Edition)', 'My Name Is Jonas', id='deluxe-id'
            ),
            SimpleTrackNapster.build(
                'Weezer', 'Weezer (Blue Album) (Deluxe Edition)',
                'My Name Is Jonas - (live, b-side)', id='deluxe-bside-id'
            )
        }

        self.assertSetEqual(expected, actual)
        expected_url = 'http://api.napster.com/v2.2/search/verbose'
        expected_query_params = 'apikey=api-key&query=Weezer+My+Name+Is+Jonas&type=track'
        expected_headers = {'Authorization': 'Bearer access-token'}
        mock_get.assert_called_with(expected_url, expected_query_params, headers=expected_headers)
