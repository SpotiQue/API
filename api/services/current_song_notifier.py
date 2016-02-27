import asyncio
import json
from ._websockets_notifier import WebsocketsNotifier


class CurrentSongNotifier(WebsocketsNotifier):

    @classmethod
    @asyncio.coroutine
    def create(cls, queue_notifier, queue_manager):
        obj = yield from super().create()
        obj.queue_notifier = queue_notifier
        obj.queue_manager = queue_manager
        return obj

    def format_message(self, title):
        return json.dumps({"title": title})

    @asyncio.coroutine
    def notify(self, message):
        queue = yield from self.queue_manager.get_queue()
        yield from self.queue_notifier.notify(queue)
        yield from super().notify(message)
