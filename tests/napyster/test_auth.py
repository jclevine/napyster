from unittest import TestCase
from src.napyster import get_access_token, refresh_api_token
from unittest.mock import patch
from uuid import UUID
from tests.common import mock_response
from unittest.mock import ANY


MOCK_CODE = '00000000-0000-0000-0000-000000000000'
MOCK_STATE = '11111111-1111-1111-1111-111111111111'


class TestAuth(TestCase):
    @patch('src.napyster.auth.input', side_effect=[MOCK_CODE, MOCK_STATE])
    @patch('src.napyster.auth.webbrowser.open_new_tab')
    @patch('src.napyster.auth.requests.post', return_value=mock_response('my-token', 'so-fresh-so-clean'))
    def test_given_you_need_a_new_token_when_you_ask_for_a_token_then_you_get_one(self, mock_post, _, ___):
        """
        Given you need a new token
         When you ask for a token
         Then you get one
        """
        actual = get_access_token(api_key='api-key', api_secret='secret', state=UUID(MOCK_STATE))
        expected = {
            'client_id': 'api-key', 'client_secret': 'secret', 'response_type': 'code',
            'grant_type': 'authorization_code', 'redirect_uri': 'localhost',
            'code': MOCK_CODE
        }
        mock_post.assert_called_with(ANY, data=expected)
        self.assertDictEqual({'access_token': 'my-token', 'refresh_token': 'so-fresh-so-clean'}, actual)

    @patch('src.napyster.auth.input', side_effect=[MOCK_CODE, MOCK_STATE])
    @patch('src.napyster.auth.webbrowser.open_new_tab')
    @patch('src.napyster.auth.requests.post', return_value=mock_response('my-token', 'so-fresh-so-clean'))
    def test_given_you_have_a_refresh_token_when_you_refresh_the_token_then_you_get_a_fresh_one(self, mock_post, _, __):
        """
        Given you have a refresh token
         When you refresh the token
         Then you get a fresh one
        """
        actual = refresh_api_token('api-key', 'secret', 'so-fresh-so-clean')
        expected = {
            'client_id': 'api-key',
            'client_secret': 'secret',
            'response_type': 'code',
            'refresh_token': 'so-fresh-so-clean',
            'grant_type': 'refresh_token',
            'redirect_uri': 'localhost'
        }
        mock_post.assert_called_with(ANY, data=expected)
        self.assertDictEqual({'access_token': 'my-token', 'refresh_token': 'so-fresh-so-clean'}, actual)

    @patch('src.napyster.auth.input', side_effect=[MOCK_CODE, MOCK_STATE])
    @patch('src.napyster.auth.webbrowser.open_new_tab')
    def test_when_you_ask_for_token_and_the_state_is_invalid_then_raise_exception(self, _, __):
        """
        Given you ask for a token
         When the state is invalid
         Then a value error is raised
        """
        self.assertRaises(ValueError, get_access_token, 'api-key', 'api_secret', 'i-sent-this')
