from unittest import TestCase
from src.napyster.auth import _get_cached_tokens


class TestTokenCache(TestCase):
    def test_given_you_have_neither_token_cached_when_you_get_cached_tokens_then_you_get_neither(self):
        """
        Given you have neither token cached
         When you get the cached tokens
         Then you get neither token
        """
        actual = _get_cached_tokens(last_token_path='dne', refresh_token_path='dne')
        self.assertDictEqual({'access_token': None, 'refresh_token': None}, actual)

    def test_given_you_have_only_the_last_token_when_you_get_cached_tokens_then_you_only_get_the_last_token(self):
        """
        Given you have only the last token
         When you get the cached tokens
         Then you only get the last token
        """
        actual = _get_cached_tokens(last_token_path='tests/.test_token', refresh_token_path='dne')
        self.assertDictEqual({'access_token': 'i-am-only-a-test-token', 'refresh_token': None}, actual)

    def test_given_you_have_only_the_refresh_token_when_you_get_cached_tokens_then_you_only_get_the_refresh_token(self):
        """
        Given you only have the refresh token
         When you get the cached tokens
         Then you only get the refresh token
        """
        actual = _get_cached_tokens(last_token_path='dne', refresh_token_path='tests/.test_token')
        self.assertDictEqual({'access_token': None, 'refresh_token': 'i-am-only-a-test-token'}, actual)

    def test_given_you_have_both_tokens_when_you_get_cached_tokens_then_you_get_both_tokens(self):
        """
        Given you have both tokens
         When you get the cached tokens
         Then you get both tokens
        """
        actual = _get_cached_tokens(last_token_path='tests/.test_token', refresh_token_path='tests/.test_token2')
        self.assertDictEqual(
            {'access_token': 'i-am-only-a-test-token', 'refresh_token': 'i-am-only-a-test-token-but-2'},
            actual
        )
