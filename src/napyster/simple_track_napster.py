from src.simple_track import SimpleTrack


class SimpleTrackNapster(SimpleTrack):
    def __init__(self, track):
        self._track = track

    @classmethod
    def build(cls, artist_name, album_title, title, id=0):
        return cls.build_from_piped_info('{}||{}||{}'.format(artist_name, album_title, title), id=id)

    @staticmethod
    def build_from_piped_info(piped_info, id=0):
        info = piped_info.split('||')
        return SimpleTrackNapster({
            'id': id,
            'name': info[2],
            'artistName': info[0],
            'albumName': info[1]
        })

    @property
    def id(self):
        return self._track['id']

    @property
    def artist_name(self):
        return self._track['artistName']

    @property
    def album_title(self):
        return self._track['albumName']

    @property
    def title(self):
        return self._track['name']

    def __repr__(self):
        return super(SimpleTrackNapster, self).__repr__()

    def __str__(self):
        return self.__repr__()
