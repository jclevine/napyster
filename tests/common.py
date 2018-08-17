from unittest.mock import MagicMock, PropertyMock


def mock_auth_response(access_token, refresh_token):
    response = MagicMock()
    type(response).text = PropertyMock(
        return_value='{{"access_token": "{}", "refresh_token": "{}"}}'.format(access_token, refresh_token)
    )
    return response


# TODO: jlevine - Allow person to pass in dict rather than json string
def mock_single_search_answer_response(json_response):
    response = MagicMock()
    type(response).text = PropertyMock(
        return_value=json_response
    )
    return response
