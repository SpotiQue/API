import asyncio
from aiohttp import web
from .services import service_registry
from .utils import json_view
import logging


@json_view
@asyncio.coroutine
def add_track_to_queue(request: web.Request):
    data = yield from request.json()
    queue_manager = yield from service_registry.get("queue_manager")
    uri = data["uri"]
    track = yield from queue_manager.add_to_queue(uri)
    logging.debug("User {} added song {} - {}".format(request.headers["X-Forwarded-For"], track.artists, track.title))
    return {"status": "ok"}
