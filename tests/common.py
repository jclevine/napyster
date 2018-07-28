from unittest.mock import MagicMock, PropertyMock


def mock_response(access_token, refresh_token):
    response = MagicMock()
    type(response).text = PropertyMock(
        return_value='{{"access_token": "{}", "refresh_token": "{}"}}'.format(access_token, refresh_token)
    )
    return response
