
import time
import uasyncio as asyncio
from config import config, pinout

from machine import Pin
from neopixel import NeoPixel
from mqtt_as import MQTTClient
from remote_light import LEDStrip, MQTTLed


# pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
# np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
# np[0] = (255, 255, 255)  # set the first pixel to white
# np.write()              # write data to all pixels
# r, g, b = np[0]         # get first pixel colour


led_strip = LEDStrip(pinout.PIN_LED1, 60)
led_strip.fill((0, 0, 0, 0))
led_strip.update()
firstSet = True


async def main():
    # await client.connect()
    while True:
        await asyncio.sleep(5)


async def publish(topic, msg):
    print("Publish - {} -> {}".format(topic, msg))
    # TODO Send and call async
    await client.publish(topic, msg)


def callback(topic_val, msg_val, retained):
    global led_strip, firstSet, client
    topic: string = topic_val.decode('ascii')
    msg = msg_val.decode('ascii')
    filter = "iot/0/benjamin/lichtleiste/0/licht/"
    if not topic.startswith(filter):
        return
    val = topic.split(filter)[1]
    setFlag = False
    if val.endswith("/set"):
        setFlag = True
        val = val.split("/set")[0]

    print("{} set to {} ({})".format(val, msg, setFlag))
    if setFlag or firstSet:
        if val == 'state':
            led_strip.set_state(msg == 'true')
            if setFlag:
                t = filter+'state'
                asyncio.get_event_loop().create_task(publish(t, msg))

        elif val == 'rgbw':
            b = int(msg)
            (r, g, b, w) = (b >> 24, b >> 16 & 0xff, b >> 8 & 0xff, b & 0xff)
            led_strip.set_rgbw((r, g, b, w))
            if setFlag:
                t = filter+'rgbw'
                asyncio.get_event_loop().create_task(publish(t, msg))


async def conn_han(client: MQTTClient):
    await client.subscribe('iot/0/benjamin/lichtleiste/0/licht/#', 1)
    # await client.subscribe('iot/0/office/#', 1)


def ready():
    print("=================R==E==A==D==Y========")


async def first_delay():
    global firstSet
    await asyncio.sleep(20)
    firstSet = False
    print("Initial Phase ended")

client = None


def run():
    global client
    loop = asyncio.get_event_loop()
    client = MQTTLed(config, callback, conn_han, 'iot/0/benjamin/lichtleiste/0/licht/connect', ready)
    loop = asyncio.get_event_loop()
    loop.create_task(client.loop())
    loop.create_task(first_delay())

    # TODO: LED Loop fpr frame effects
    try:
        loop.run_until_complete(main())
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors


MQTTClient.DEBUG = True
run()
