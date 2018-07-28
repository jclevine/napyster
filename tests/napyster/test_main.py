from unittest import TestCase
from src.napyster.main import main
from unittest.mock import patch, call
import os


@patch.dict(os.environ, {'API_KEY': 'api-key', 'API_SECRET': 'secret'})
@patch('src.napyster.main.uuid4', return_value='fake-uuid')
@patch('src.napyster.main.write_token_to_filepath')
class TestMain(TestCase):

    @patch('src.napyster.main.get_access_token',
           return_value={'access_token': 'new-token', 'refresh_token': 'even-fresher'})
    def test_given_only_have_last_token_when_you_run_then_you_need_to_get_entirely_new_token(
            self, mock_get_access_token, mock_write, _):
        """
        Given you only have the last token
         When you run main
         Then you need to get an entirely new token
          and you save it to the cache file
        """
        actual = main(last_token_path='tests/.test_token', refresh_token_path='dne')
        expected = {'api_key': 'api-key', 'api_secret': 'secret', 'state': 'fake-uuid'}
        mock_get_access_token.assert_called_with(**expected)
        self.assertDictEqual({'access_token': 'new-token', 'refresh_token': 'even-fresher'}, actual)
        mock_write.assert_has_calls(
            [call('.last_token', 'new-token'), call('.refresh_token', 'even-fresher')]
        )

    @patch('src.napyster.main.refresh_api_token',
           return_value={'access_token': 'new-token', 'refresh_token': 'even-fresher'})
    def test_given_only_have_refresh_token_when_you_run_then_you_refresh_the_token(
            self, mock_refresh_token, mock_write, _):
        """
        Given you only have a refresh token
         When you run main
         Then you refresh the token
          and you save the access token to the cache file
        """
        actual = main(last_token_path='dne', refresh_token_path='tests/.test_token')
        expected = {
            'api_key': 'api-key',
            'api_secret': 'secret',
            'refresh_token': 'i-am-only-a-test-token',
        }
        mock_refresh_token.assert_called_with(**expected)
        self.assertDictEqual({'access_token': 'new-token', 'refresh_token': 'even-fresher'}, actual)
        mock_write.assert_called_once_with('.last_token', 'new-token')

    @patch('src.napyster.main.get_access_token',
           return_value={'access_token': 'new-token', 'refresh_token': 'super-fresh'})
    def test_given_do_not_have_any_tokens_when_you_run_then_you_get_the_token(self, mock_get_token, mock_write, _):
        """
        Given you don't have any tokens
         When you run main
         Then you get the token
          and you save both to the cache file
        """
        actual = main(last_token_path='dne', refresh_token_path='dne')
        expected = {
            'api_key': 'api-key',
            'api_secret': 'secret',
            'state': 'fake-uuid',
        }
        mock_get_token.assert_called_with(**expected)
        self.assertDictEqual({'access_token': 'new-token', 'refresh_token': 'super-fresh'}, actual)
        mock_write.assert_has_calls(
            [call('.last_token', 'new-token'), call('.refresh_token', 'super-fresh')]
        )

    @patch('src.napyster.main.get_access_token')
    def test_given_you_have_both_tokens_when_you_run_then_you_get_the_same_tokens(self, mock_get_token, mock_write, _):
        """
        Given you have both tokens
         When you run main
         Then you get the same tokens
          and you don't save either
        """
        actual = main(last_token_path='tests/.test_token', refresh_token_path='tests/.test_token2')
        mock_get_token.assert_not_called()
        mock_write.assert_not_called()
        self.assertDictEqual(
            {'access_token': 'i-am-only-a-test-token', 'refresh_token': 'i-am-only-a-test-token-but-2'}, actual
        )
