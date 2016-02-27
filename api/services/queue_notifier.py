import json
from ._websockets_notifier import WebsocketsNotifier


class QueueNotifier(WebsocketsNotifier):

    def __init__(self):
        super().__init__()

    def format_message(self, queue):
        return json.dumps([track.to_json(minimal=True) for track in queue])
