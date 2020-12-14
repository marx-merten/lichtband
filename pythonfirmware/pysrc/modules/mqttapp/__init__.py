from .utils import schedule
import ubinascii
from mqtt_as import MQTTClient
import uasyncio as asyncio
import network
from picoweb import WebApp
import web.web_sys as sysapp


class MQTTApplication:
    def __init__(self, config, prefix="", online_suffix="", debug=False):
        self.debug = debug
        MQTTClient.DEBUG = debug

        config['subs_cb'] = self.cb_msg
        config['connect_coro'] = self.cb_connect
        self.prefix = prefix
        self.suffix = {}
        self.suffix['online'] = online_suffix
        self.online_topic = prefix+online_suffix
        self.online = False
        self.mqtt = MQTTClient(config)
        self.cfg = config
        self.should_stop = False
        self.subscribers = {}
        self.started_callbacks = []

    async def loop(self):
        await asyncio.sleep_ms(100)
        print("Connecting to MQQT ({}:{})".format(self.cfg['server'], self.cfg['port']))
        await self.mqtt.connect()
        print("DONE ({})".format(self.cfg['server']))
        if self.online_topic != "":
            schedule(self._send_connect_msg())
        schedule(self.cb_started())
        print("Done")

    def run(self, cb=None):
        loop = asyncio.get_event_loop()
        loop.create_task(self.loop())
        if cb == None:
            cb = self._while_not_stopped
        try:
            loop.run_until_complete(cb())
        finally:
            self.mqtt.close()  # Prevent LmacRxBlk:1 errors

    async def publish(self, topic, msg):
        print("Publish - {} -> {}".format(topic, msg))
        await self.mqtt.publish(topic, msg)

    def stop(self):
        # just a flag at this point
        self.should_stop = True

    def add_ready_callback(self, cb):
        self.started_callbacks.append(cb)

    def subscribe(self, filter: string, callback):
        if filter in self.subscribers.keys():
            return
        if not filter.startswith('/') and self.prefix == "":
            raise Exception("For use of relative subscribes a prefix need to be set")
        # TODO: Better check that also captures bound methods :<class 'bound_method'>
        # if not type(callback).__name__ == 'generator':
        #     raise Exception("async function reference required {}".format(type(callback)))
        self.subscribers[filter] = callback
        if filter.startswith('/'):
            pass
            # TODO: Adhoc subscribe required

    # Basic msg callback,
    def cb_msg(self, topic_val, msg_val, retained):
        topic: string = topic_val.decode('ascii')
        msg = msg_val.decode('ascii')
        if not topic.startswith('/'):
            topic = '/'+topic
        print("{} set to {} ({})".format(topic, msg, retained))
        processed = False
        for f in self.subscribers.keys():
            if not f.startswith('/'):
                filter = "/"+self.prefix+f
            else:
                filter = f
            if topic.startswith(filter):
                stopic = topic[len(filter):]
                schedule(self.subscribers[f](topic, stopic, msg, retained))
                processed = True
        if not processed:
            print("...unprocessed")

    # Basic Connect
    async def cb_connect(self, client: MQTTClient):
        print("Register subscribers")
        if self.prefix and self.prefix != "":
            await self.mqtt.subscribe(self.prefix+"#", qos=1)
        for k in self.subscribers.keys():
            if k.startswith('/'):
                pass
                # TODO: handle all subscriber connect  if not within prefix, register to prefix if not empty

    async def cb_started(self):
        if self.prefix and self.prefix != "":
            sta_if = network.WLAN(network.STA_IF)
            (ip, mask, _, dns) = sta_if.ifconfig()
            print("-- IP Address : {} : {}".format(ip, mask))
            print("-- DNS Server : {}".format(dns))
            schedule(self.publish(self.prefix+'device/ip', "{}".format(ip)))
            mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
            schedule(self.publish(self.prefix+'device/mac', "{}".format(mac)))
        for cb in self.started_callbacks:
            cb()

    async def _send_connect_msg(self):
        print("Sending Connect Notification")
        await asyncio.sleep(1)
        await self.mqtt.publish(self.online_topic, 'true', qos=1)

    async def _while_not_stopped(self, delay=5):
        while not self.should_stop:
            await asyncio.sleep(delay)


class MQTTWebApplication(MQTTApplication):
    def __init__(self, config, prefix="", online_suffix="", debug=False, web_port=80, sys_app=True):
        super().__init__(config, prefix, online_suffix, debug)
        self.web_port = web_port
        self.web = WebApp(__name__)
        self.web.mount("/kernel", sysapp.app)

    async def cb_started(self):
        await super().cb_started()
        self.web.run(host='0.0.0.0', port=self.web_port, debug=self.debug)
