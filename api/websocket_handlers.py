import asyncio
import aiohttp
from aiohttp import web
from .services import service_registry


@asyncio.coroutine
def websocket_handler(request: web.Request, notifier):
    connection = web.WebSocketResponse()
    yield from connection.prepare(request)

    yield from notifier.add_connection(connection)

    while not connection.closed:
        msg = yield from connection.receive()
        if msg.tp == aiohttp.MsgType.text and msg.data == 'close':
            yield from connection.close()

    yield from notifier.remove_connection(connection)

    return connection


@asyncio.coroutine
def queue_handler(request):
    notifier = yield from service_registry.get("queue_notifier")
    return_value = yield from websocket_handler(request, notifier)
    return return_value


@asyncio.coroutine
def current_song_handler(request):
    notifier = yield from service_registry.get("current_song_notifier")
    return_value = yield from websocket_handler(request, notifier)
    return return_value
