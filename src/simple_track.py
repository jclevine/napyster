class SimpleTrack:
    @property
    def id(self):
        raise NotImplementedError()

    @property
    def artist_name(self):
        raise NotImplementedError()

    @property
    def album_title(self):
        raise NotImplementedError()

    @property
    def title(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, SimpleTrack):
            return (self.artist_name == other.artist_name and
                    self.album_title == other.album_title and
                    self.title == other.title)

        return NotImplemented

    @property
    def __dict__(self):
        return {
            'artist_name': self.artist_name, 'album_title': self.album_title, 'title': self.title
        }

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return '{}||{}||{}'.format(self.artist_name, self.album_title, self.title)

    def __str__(self):
        return self.__repr__()
