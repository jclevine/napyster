from unittest.mock import MagicMock, PropertyMock


def mock_auth_response(access_token, refresh_token):
    response = MagicMock()
    type(response).text = PropertyMock(
        return_value='{{"access_token": "{}", "refresh_token": "{}"}}'.format(access_token, refresh_token)
    )
    return response


def mock_single_search_answer_response():
    response = MagicMock()
    type(response).text = PropertyMock(
        return_value='{"search":{"data":{"tracks":[{"type":"track","id":"tra.68944077",'
                     '"name":"Quick Canal","artistName":"Atlas Sound","albumName":"Logos"}]}}}'
    )
    return response
