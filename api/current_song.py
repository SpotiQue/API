import asyncio
from .services import service_registry


@asyncio.coroutine
def listen_for_song_changed(reader, writer):
    data = yield from reader.read()
    message = data.decode()

    current_song_notifier = yield from service_registry.get("current_song_notifier")
    yield from current_song_notifier.notify(message)
