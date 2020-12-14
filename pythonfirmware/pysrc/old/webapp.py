import picoweb
import uasyncio as asyncio
import gc
import ujson
from uhashlib import sha256
import ubinascii

import web.web_sys as sysapp


class Server (picoweb.WebApp):
    def __init__(self, pkg, routes=None, serve_static=True):
        super().__init__(pkg, routes, serve_static)

    def serve(self, loop, host, port):
        loop.create_task(asyncio.start_server(self._handle, host, port))
        # loop.run_forever()


site = Server(__name__)


@site.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<h1> WELCOME</h1>")


site.mount("/kernel", sysapp.app)
