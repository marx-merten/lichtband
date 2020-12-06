from machine import Pin
from time import sleep_ms
import uasyncio as asyncio

from mqtt_as import MQTTClient
from neopixel import NeoPixel


class LEDStrip:
    def __init__(self, pin_led, count):
        self.led = Pin(pin_led, Pin.OUT)
        self.count = count
        self.pixel = NeoPixel(self.led, self.count, bpp=4)
        self.rgbw = (50, 0, 0, 0)
        self.state = False

    def fill(self, color: tuple):
        print("LED set to fill color {}".format(color))
        self.pixel.fill(color)
        return self

    def update(self):
        self.pixel.write()

    def set_state(self, new_state: boolean):
        print(" STATE {} -> {}".format(self.state, new_state))
        if new_state == self.state:
            return
        self.state = new_state
        if self.state == True:
            self.fill(self.rgbw)
        else:
            self.fill((0, 0, 0, 0))
        self.update()

    def set_rgbw(self, color):
        self.rgbw = color
        if self.state:
            self.fill(color)
            self.update()


class MQTTLed:
    def __init__(self, config, callback, conn_han, online_topic, finish_cb=None):
        config['subs_cb'] = callback
        config['connect_coro'] = conn_han
        self.config = config
        self.mqtt = MQTTClient(config)
        self.online_topic = online_topic
        self.finish_cb = finish_cb

    async def loop(self):
        await asyncio.sleep_ms(100)
        print("Connecting to MQQT ({}:{})".format(self.config['server'], self.config['port']))
        await self.mqtt.connect()
        print("DONE ({})".format(self.config['server']))
        await asyncio.sleep(2)
        print("Sending Connect Notification")
        await asyncio.sleep(1)
        await self.mqtt.publish(self.online_topic, 'true', qos=1)
        if self.finish_cb:
            self.finish_cb()
        print("Done")

    async def publish(self, topic, msg):
        print("Sending to {}".format(topic))
        await self.mqtt.publish(topic, msg, qos=1)
        print("Done [{}]".format(msg))

    def close(self):
        self.mqtt.close()
