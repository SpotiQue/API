import asyncio
import abc


class WebsocketsNotifier(metaclass=abc.ABCMeta):

    def __init__(self):
        self.connections = set()
        self.last_message = ""

    @abc.abstractmethod
    def format_message(self, message):
        pass

    @classmethod
    @asyncio.coroutine
    def create(cls):
        return cls()

    @asyncio.coroutine
    def add_connection(self, connection):
        self.connections.add(connection)
        connection.send_str(self.last_message)

    @asyncio.coroutine
    def remove_connection(self, connection):
        self.connections.remove(connection)

    @asyncio.coroutine
    def notify(self, message):
        message = self.last_message = self.format_message(message)
        for connection in self.connections:
            connection.send_str(message)

    @asyncio.coroutine
    def close_connections(self):
        for connection in self.connections:
            yield from connection.close(code=999, message="server shutdown")
