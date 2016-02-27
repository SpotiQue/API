import asyncio
from aiohttp import web
from .queue import add_track_to_queue
from .search import search
from .services import service_registry
from .websocket_handlers import current_song_handler, queue_handler
from .current_song import listen_for_song_changed
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(message)s')




class APIApplication(web.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tcp_server = self.loop.run_until_complete(asyncio.start_server(listen_for_song_changed, "localhost", 3403))

        self.register_routes()
        self.initialize_state()
        self.create_shutdown_callbacks()

    def register_routes(self):
        self.router.add_route('POST', '/queue', add_track_to_queue)
        self.router.add_route('GET', '/search', search)

        self.router.add_route('GET', '/queue', queue_handler)
        self.router.add_route('GET', '/current_song', current_song_handler)

    def initialize_state(self):
        """
        This method downloads current queue from redis and notifies all the sockets connected.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(service_registry.get("queue_manager"))

    @asyncio.coroutine
    def shutdown_websockets(self, app):
        queue_notifier = yield from service_registry.get("queue_notifier")
        current_song_notifier = yield from service_registry.get("current_song_notifier")
        yield from queue_notifier.close_connections()
        yield from current_song_notifier.close_connections()

    def create_shutdown_callbacks(self):
        self.on_shutdown.append(self.shutdown_websockets)
