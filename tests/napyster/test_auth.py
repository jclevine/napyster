from unittest import TestCase
from src.napyster.auth import _get_new_access_tokens, _refresh_api_token
from src.napyster.auth import get_access_tokens
from unittest.mock import patch, call
from uuid import UUID
from tests.common import mock_response
from unittest.mock import ANY
import os


MOCK_CODE = '00000000-0000-0000-0000-000000000000'
MOCK_STATE = '11111111-1111-1111-1111-111111111111'


@patch.dict(os.environ, {'API_KEY': 'api-key', 'API_SECRET': 'secret'})
@patch('src.napyster.auth.uuid4', return_value='fake-uuid')
@patch('src.napyster.auth.input', side_effect=[MOCK_CODE, MOCK_STATE])
@patch('src.napyster.auth.webbrowser.open_new_tab')
@patch('src.napyster.auth.requests.post', return_value=mock_response('my-token', 'so-fresh-so-clean'))
class TestAuth(TestCase):
    def test_given_you_need_a_new_token_when_you_ask_for_a_token_then_you_get_one(self, mock_post, *_):
        """
        Given you need a new token
         When you ask for a token
         Then you get one
        """
        actual = _get_new_access_tokens(api_key='api-key', api_secret='secret', state=UUID(MOCK_STATE))
        expected = {
            'client_id': 'api-key', 'client_secret': 'secret', 'response_type': 'code',
            'grant_type': 'authorization_code', 'redirect_uri': 'localhost',
            'code': MOCK_CODE
        }
        mock_post.assert_called_with(ANY, data=expected)
        self.assertDictEqual({'access_token': 'my-token', 'refresh_token': 'so-fresh-so-clean'}, actual)

    def test_given_you_have_a_refresh_token_when_you_refresh_the_token_then_you_get_a_fresh_one(self, mock_post, *_):
        """
        Given you have a refresh token
         When you refresh the token
         Then you get a fresh one
        """
        actual = _refresh_api_token('api-key', 'secret', 'so-fresh-so-clean')
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

    def test_when_you_ask_for_token_and_the_state_is_invalid_then_raise_exception(self, *_):
        """
        Given you ask for a token
         When the state is invalid
         Then a value error is raised
        """
        self.assertRaises(ValueError, _get_new_access_tokens, 'api-key', 'api_secret', 'i-sent-this')

    @patch('src.napyster.auth.write_token_to_filepath')
    @patch('src.napyster.auth._get_new_access_tokens',
           return_value={'access_token': 'new-token', 'refresh_token': 'even-fresher'})
    def test_given_only_have_last_token_when_you_run_then_you_need_to_get_entirely_new_token(
            self, mock_get_access_token, mock_write, *_):
        """
        Given you only have the last token
         When you run main
         Then you need to get an entirely new token
          and you save it to the cache file
        """
        actual = get_access_tokens(last_token_path='tests/.test_token', refresh_token_path='dne')
        expected = {'api_key': 'api-key', 'api_secret': 'secret', 'state': 'fake-uuid'}
        mock_get_access_token.assert_called_with(**expected)
        self.assertDictEqual({'access_token': 'new-token', 'refresh_token': 'even-fresher'}, actual)
        mock_write.assert_has_calls(
            [call('.last_token', 'new-token'), call('.refresh_token', 'even-fresher')]
        )

    @patch('src.napyster.auth.get_access_tokens')
    def test_given_you_have_both_tokens_when_you_run_then_you_get_the_same_tokens(self, mock_get_token, mock_write, *_):
        """
        Given you have both tokens
         When you run main
         Then you get the same tokens
          and you don't save either
        """
        actual = get_access_tokens(last_token_path='tests/.test_token', refresh_token_path='tests/.test_token2')
        mock_get_token.assert_not_called()
        mock_write.assert_not_called()
        self.assertDictEqual(
            {'access_token': 'i-am-only-a-test-token', 'refresh_token': 'i-am-only-a-test-token-but-2'}, actual
        )

    @patch('src.napyster.auth.write_token_to_filepath')
    @patch('src.napyster.auth._refresh_api_token',
           return_value={'access_token': 'new-token', 'refresh_token': 'even-fresher'})
    def test_given_only_have_refresh_token_when_you_run_then_you_refresh_the_token(
            self, mock_refresh_token, mock_write, *_):
        """
        Given you only have a refresh token
         When you run main
         Then you refresh the token
          and you save the access token to the cache file
        """
        actual = get_access_tokens(last_token_path='dne', refresh_token_path='tests/.test_token')
        expected = {
            'api_key': 'api-key',
            'api_secret': 'secret',
            'refresh_token': 'i-am-only-a-test-token',
        }
        mock_refresh_token.assert_called_with(**expected)
        self.assertDictEqual({'access_token': 'new-token', 'refresh_token': 'even-fresher'}, actual)
        mock_write.assert_called_once_with('.last_token', 'new-token')
