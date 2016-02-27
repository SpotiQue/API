
class Track:

    def __init__(self, title, artists, uri, skip_count=0, is_queued=False, cover_url="", duration="",):
        self.title = title
        self.artists = artists
        self.uri = uri
        self.cover_url = cover_url
        self.duration = duration
        self.skip_count = skip_count
        self.is_queued = is_queued

    def to_json(self, minimal=False):
        included_keys = {"title", "artists", "uri"}
        if not minimal:
            included_keys |= {"cover_url", "duration"}
        return {k: v for k, v in self.__dict__.items() if k in included_keys}
