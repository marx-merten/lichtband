
import time
import uasyncio as asyncio
from config import config, pinout
from mqttapp.utils import schedule
from machine import Pin
from neopixel import NeoPixel
from mqtt_as import MQTTClient
from remote_light import LEDStrip, MQTTLed
import esp32
from esp32 import Partition
import network
import ubinascii
import webapp


# pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
# np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
# np[0] = (255, 255, 255)  # set the first pixel to white
# np.write()              # write data to all pixels
# r, g, b = np[0]         # get first pixel colour

# TODO: Change to propper management
led_strip = LEDStrip(pinout.PIN_LED1, config['leds'])
led_strip.fill((0, 0, 0, 0))
led_strip.update()
firstSet = True


# Main Loop . uasyncio will run this and it will be a exit point if needed
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
    filter = config['prefix']+'licht/'
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
                schedule(publish(t, msg))

        elif val == 'rgbw':
            b = int(msg)
            (r, g, b, w) = (b >> 24, b >> 16 & 0xff, b >> 8 & 0xff, b & 0xff)
            led_strip.set_rgbw((r, g, b, w))
            if setFlag:
                t = filter+'rgbw'
                asyncio.get_event_loop().create_task(publish(t, msg))


async def conn_han(client: MQTTClient):
    await client.subscribe(config['prefix']+'licht/#', 1)

    await client.subscribe('iot/0/office/#', 1)


def ready():
    print("=================R==E==A==D==Y========")
    sta_if = network.WLAN(network.STA_IF)
    (ip, mask, _, dns) = sta_if.ifconfig()
    print("-- IP Address : {} : {}".format(ip, mask))
    print("-- DNS Server : {}".format(dns))
    schedule(publish(config['prefix']+'device/ip', "{}".format(ip)))
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    schedule(publish(config['prefix']+'device/mac', "{}".format(mac)))

    # def run(self, host="127.0.0.1", port=8081, debug=False, lazy_init=False, log=None):
    webapp.site.run(host="0.0.0.0", port=80, debug=True)
    schedule(first_delay())
    # TODO: Need to find a better solution to test for the verification when really doing OTA
    print("=== Active Partition {}".format(Partition(Partition.RUNNING).info()))
    Partition.mark_app_valid_cancel_rollback()


async def first_delay():
    global firstSet
    await asyncio.sleep(60)
    firstSet = False
    print("Initial Phase ended")

client = None


def run():
    global client
    loop = asyncio.get_event_loop()
    client = MQTTLed(config, callback, conn_han, config['prefix']+'device/connect', ready)
    loop = asyncio.get_event_loop()
    loop.create_task(client.loop())

    # TODO: LED Loop fpr frame effects
    try:
        loop.run_until_complete(main())
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors


MQTTClient.DEBUG = True


run()
