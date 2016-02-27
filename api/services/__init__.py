import asyncio
from .queue_manager import QueueManager
from .queue_notifier import QueueNotifier
from .web_api import WebAPI
from .current_song_notifier import CurrentSongNotifier

class ServiceNotRegisteredError(Exception):
    pass


class ServiceRegistry:

    def __init__(self):
        self._services = {}

    def register(self, name, cls, *dependencies):
        self._services[name] = {
            "cls": cls,
            "instance": None,
            "dependencies": dependencies
        }

    @asyncio.coroutine
    def get(self, name):
        if name not in self._services:
            raise ServiceNotRegisteredError()

        service_entry = self._services[name]
        if not service_entry["instance"]:

            dependencies = []
            for dependency in service_entry["dependencies"]:
                dependency = yield from self.get(dependency)
                dependencies.append(dependency)

            service_entry["instance"] = yield from service_entry["cls"].create(*dependencies)

        return service_entry["instance"]


service_registry = ServiceRegistry()


def register_services():
    service_registry.register("queue_notifier", QueueNotifier)
    service_registry.register("queue_manager", QueueManager, "queue_notifier", "web_api")
    service_registry.register("web_api", WebAPI)
    service_registry.register("current_song_notifier", CurrentSongNotifier, "queue_notifier", "queue_manager")

register_services()
