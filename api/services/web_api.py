import asyncio
import aiohttp
from ..models.track import Track
from urllib.parse import urlencode


class WebAPI:

    base_url = "https://api.spotify.com/v1"

    @classmethod
    @asyncio.coroutine
    def create(cls):
        return cls()

    @staticmethod
    def _convert_duration(time):
        time /= 60000
        return "{:02}:{:02}".format(int(time), int(time*6))

    def convert_to_track(self, track):
        cover = track["album"]["images"]
        if cover:
            cover = cover[-1]["url"]
        return Track(
            title=track["name"],
            duration=self._convert_duration(track["duration_ms"]),
            artists=", ".join(artist["name"] for artist in track["artists"]),
            uri=track["uri"],
            cover_url=cover or "",
        )

    @asyncio.coroutine
    def get_track_info(self, track_uri):
        track_id = track_uri.split(":")[-1]
        url = "/".join((self.base_url, "tracks", track_id))
        track = yield from self._fetch_json(url)
        return self.convert_to_track(track)

    @asyncio.coroutine
    def search_tracks(self, query):
        if not query:
            return []
        query = urlencode({
            "q": query,
            "market": "PL",
            "type": "track"
        })
        url = "/".join((self.base_url, "search?{}".format(query)))
        response = yield from self._fetch_json(url)
        return (self.convert_to_track(track) for track in response["tracks"]["items"])

    @staticmethod
    @asyncio.coroutine
    def _fetch_json(url):
        with aiohttp.ClientSession() as session:
            with aiohttp.Timeout(10):
                resp = yield from session.get(url)
                assert resp.status == 200
                json_data = yield from resp.json()
                return json_data
