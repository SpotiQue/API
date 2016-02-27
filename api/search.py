import asyncio
from aiohttp import web
from api.services import service_registry
from .utils import json_view


@json_view
@asyncio.coroutine
def search(request: web.Application):
    query = request.GET["q"]
    web_api = yield from service_registry.get("web_api")
    tracks = yield from web_api.search_tracks(query)
    return [track.to_json() for track in tracks]
