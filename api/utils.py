import asyncio
from aiohttp import web
from functools import wraps
import json


def json_view(f):
    @wraps(f)
    @asyncio.coroutine
    def _wrapper(*args, **kwargs):
        ret_val = yield from f(*args, **kwargs)
        return web.Response(body=json.dumps(ret_val).encode(), content_type="application/json")
    return _wrapper
