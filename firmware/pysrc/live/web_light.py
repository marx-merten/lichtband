import ulogging as logging
import picoweb
import ujson
from uhashlib import sha256
import ubinascii
import re
import uos as os
from picoweb.utils import parse_qs
from web.utils import _json_error, _json_msg, _json_response, _txt_response
from picoweb import http_error
from ledstrip import Band as LEDBand


import utime as time



# Default Logging
LOG = logging.getLogger(__name__)
corsHeader = {'Access-Control-Allow-Origin': '*'}


class LightWeb:
    def __init__ (self, lb:LEDBand,cb_update):
        self.lichtband=lb
        self.app = picoweb.WebApp(__name__)
        self.app.add_url_rule("/status",self.web_status)
        self.app.add_url_rule("/switch",self.web_switch)
        self.cb_update=cb_update



    async def web_status(self,req,resp):
        lichtstatus = {}
        lichtstatus['state'] = self.lichtband.state
        lichtstatus['rgbw'] = self.lichtband.rgbw
        lichtstatus['sceneState'] = self.lichtband.isActiveScene()
        if self.lichtband.isActiveScene() :
            lichtstatus['activeScene'] = self.lichtband.activeScene.getName()
        else :
            lichtstatus['activeScene'] = "None"
        lichtstatus['scenes'] = list(self.lichtband.scenes.keys())

        await _json_response(resp,lichtstatus,headers=corsHeader)

    async def web_switch(self,req,resp):
        req.parse_qs()
        state = False
        if ('state' in req.form.keys()):
            state = req.form['state'].lower() in ['yes', 'true', '1']
            self.lichtband.set(state=state)
            self.lichtband.update()
            if self.cb_update is not None:
                self.cb_update()
            await _json_response(resp,{'switched':state},headers=corsHeader)
        if ('scene' in req.form.keys()):
            scene = req.form['scene']
            self.lichtband.activateScene(scene)
            self.lichtband.set(state=True)
            self.lichtband.update()
            if self.cb_update is not None:
                self.cb_update()
            await _json_response(resp,{'switchedScene':scene},headers=corsHeader)

    def register(self,server):
        server.mount("/light",self.app)
