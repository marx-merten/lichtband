from mqttapp import MQTTApplication, MQTTWebApplication
from mqttapp.utils import schedule
from config import config, pinout, MQTT_PREFIX, ONLINE_SUFFIX, NAME
from utils import create_repeat_routine,isCommand,str_to_bool
import uasyncio as asyncio

import ledstrip
import machine
import time
from bootup import Boot

import ubinascii
import network
from fileconfig import Config

import gc

# Default Logging
import ulogging as logging
LOG = logging.getLogger(__name__)

cfg = Config()
config['ssid'] = cfg.get("network/ssid")
config['wifi_pw'] = cfg.get('network/password')
config['server'] = cfg.get('mqtt/server')
config['port'] = cfg.get('mqtt/port')


mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
mqtt = MQTTWebApplication(config,
                          prefix=cfg.get('mqtt/prefix')+cfg.get('mqtt/name')+"/",  online_suffix=cfg.get('mqtt/online'), debug=False, device_prefix="device/{}/".format(mac))


# make sure regular memory cleanup
# create_repeat_routine(gc.collect, 30000)

# Connect licht values to controll flow
try:
    lichtband = ledstrip.Band(300,machine.Pin(23),4)
except OSError:
    print("Error in sequence, while creating lightstrip data, restart in 5")
    time.sleep_ms(5000)
    machine.reset()

async def controllLightState(topic, stopic, msg, retained):
    if topic.endswith("/set"):
        lichtband.set(state=str_to_bool(msg))
        lichtband.update()
        await mqtt.publish(topic[:-4],msg)

async def controllLightRGBW(topic, stopic, msg, retained):
    if topic.endswith("/set"):
        colors = []
        for o in msg.split(','):
            colors.append(int(o))
        lichtband.set(rgbw=tuple(colors))
        lichtband.update()
        await mqtt.publish(topic[:-4],msg)


mqtt.subscribe("licht/state",controllLightState)
mqtt.subscribe("licht/rgbw",controllLightRGBW)



async def initialSync():
    asyncio.sleep_ms(1000)
    v="true" if lichtband.state else "false"
    await mqtt.publish(mqtt.prefix+"licht/state",v)
    await mqtt.publish(mqtt.prefix+"licht/rgbw",",".join([str(i) for i in lichtband.rgbw]))



boot=Boot(lichtband)
mqtt.add_ready_callback(boot.updateReady)
mqtt.add_ready_callback(lambda: schedule(initialSync()))

import scenes.basic as scene
print("Doing it")
scene.register(lichtband)
print(lichtband.scenes)
LOG.info("STARTING WEB APP")
# Starting main app main loop. Mqqt will manage the events and event-loop
mqtt.run()
