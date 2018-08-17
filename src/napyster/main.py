from src.napyster import NapsterClient
from os import environ
from src.napyster import get_access_token, SimpleTrackNapster
from src.common import get_lines_as_list


tracks_not_in_napster = [
    # SimpleTrackNapster.build_from_piped_info(
    #     'Tears for Fears||20th Century Masters: The Millennium Collection: Best Of Tears For Fears||Shout'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Depeche Mode||Playing The Angel ||John The Revelator'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Ben Folds Five||Whatever and Ever Amen||Song For The Dumped'  # Ben Folds without the Five
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Belle and Sebastian||If You’re Feeling Sinister||Judy and the Dream of Horses'  # of _the_ horses
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Clinic||Internal Wrangler||2nd Foot Stomp'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Trashcan Sinatras||Fez||Easy Read'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Buck-O-Nine||Songs In The Key Of Bree||Irish Drinking Song'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Dead Kennedys||Give Me Convenience or Give Me Death||Too Drunk to Fuck'  # F*ck
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Trashcan Sinatras||Fez||All the Dark Horses'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Pet Shop Boys||Alternative||Miserablism'
    # ),
    # SimpleTrackNapster.build_from_piped_info(
    #     'Nine Inch Nails||Broken||Physical'  # Physical (You're So)
    # )







]


if __name__ == '__main__':  # pragma: no cover
    api_key = environ['API_KEY']

    tracks = get_lines_as_list('../../all_loved_track_infos_20180722.txt')

    client = NapsterClient(api_key, get_access_token)

    # chunks = [tracks[i:i + 10] for i in range(0, len(tracks), 10)]
    for piped_track in tracks:
        track = SimpleTrackNapster.build_from_piped_info(piped_track)

        if track in tracks_not_in_napster:
            continue

        answer = client.search_for_track_by_album(track)
        if len(answer) == 1:
            print(client.mark_tracks_as_favourite([answer.pop()]))
        elif len(answer) == 0:
            print('Unable to find {}'.format(track))
        else:
            print('Too many for now: {}'.format(len(answer)))
