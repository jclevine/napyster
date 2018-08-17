from src.napyster import NapsterClient
from os import environ
from src.napyster import get_access_token, SimpleTrackNapster


if __name__ == '__main__':  # pragma: no cover
    api_key = environ['API_KEY']
    client = NapsterClient(api_key, get_access_token)
    simple_track = SimpleTrackNapster.build('Weezer', 'Weezer', 'My Name Is Jonas')
    answer = client.search_for_track_by_album(simple_track)
    print(answer)
