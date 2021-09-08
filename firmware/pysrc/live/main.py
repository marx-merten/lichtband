from mqttapp import MQTTApplication, MQTTWebApplication
from mqttapp.utils import schedule
from config import config, pinout, MQTT_PREFIX, ONLINE_SUFFIX, NAME
from utils import create_repeat_routine,isCommand,str_to_bool
from picoweb import http_error
from web_light import LightWeb
import uasyncio as asyncio
import os
import gc
import re
import esp32

import ledstrip
import machine
import time
import ntptime

import web.web_fs as web_filesystem

from bootup import Boot

import ubinascii
import network
from fileconfig import Config


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



# Mount catchall clause, any more defined url need to be mapped before this
def handle_html( req, resp):
    path = req.url_match.group(1)
    if len(path)==0:
        path="index.html"
    if path[-1] == '/' :
        path=path+"index.html"

    path = "/html/"+path
    # check for existing files AND dir
    try:
        t_mod=os.stat(path)[0]
        if t_mod==0o040000 :
            #File is dir, add index.html
            path=path+"/index.html"
    except OSError:
        print ("File Error")
        yield from http_error(resp, "404")
        return

    if ".." in path:
        yield from http_error(resp, "403")
        return
    yield from mqtt.web.sendfile(resp, path)

mqtt.web.add_url_rule(re.compile("^/(.*)"),handle_html)



# Connect licht values to controll flow
try:
    lichtband = ledstrip.Band(cfg.get('led/count'),machine.Pin(23),4)
except OSError:
    print("Error in sequence, while creating lightstrip data, restart in 5")
    time.sleep_ms(5000)
    machine.reset()




async def controllLightState(topic, stopic, msg, retained):
    if topic.endswith("/set"):
        lichtband.set(state=str_to_bool(msg))
        await sendState()

async def controllLightRGB(topic, stopic, msg, retained):
    if topic.endswith("/set"):
        colors = []
        for o in msg.split(','):
            colors.append(int(o))
        lichtband.set(rgb=tuple(colors))
        await sendState()

async def controllScene(topic, stopic, msg, retained):
    if topic.endswith("/set"):
        scene=msg
        lichtband.activateScene(scene)
        lichtband.set(state=True)
        await sendState()


mqtt.subscribe("licht/state",controllLightState)
mqtt.subscribe("licht/rgb",controllLightRGB)
mqtt.subscribe("licht/scene",controllScene)


async def sendState():
    v="true" if lichtband.state else "false"
    await mqtt.publish(mqtt.prefix+"device/scenes",",".join([ m for m in lichtband.scenes]))
    await mqtt.publish(mqtt.prefix+"licht/rgb",",".join([str(i) for i in lichtband.rgb]))
    await mqtt.publish(mqtt.prefix+"licht/state",v)
    scenenName="None"
    if lichtband.isActiveScene() :
        scenenName=lichtband.activeScene.getName()
    await mqtt.publish(mqtt.prefix+"licht/scene",scenenName)



async def initialSync():
    await asyncio.sleep_ms(1000)
    await sendState()


async def finalizePartition():
    await asyncio.sleep_ms(10000)
    print("ALLLL SEEMS OK, marking Partition good !!!!!")
    esp32.Partition.mark_app_valid_cancel_rollback()

async def ntpUpdater():
    await asyncio.sleep_ms(2000)
    try:
        ntptime.settime()
    except Exception :
        pass
    await asyncio.sleep(60*60)

async def wdtLoop():
    wdt= machine.WDT(timeout=30000)
    wdt.feed()
    while True:
        await asyncio.sleep(10)
        wdt.feed()

def starteTick():
    schedule(lichtband.tick())


boot=Boot(lichtband)
mqtt.add_ready_callback(boot.updateReady)
mqtt.add_ready_callback(lambda: schedule(initialSync()))
mqtt.add_ready_callback(lambda: schedule(ntpUpdater()))
#mqtt.add_ready_callback(lambda: schedule(wdtLoop()))
mqtt.add_ready_callback(lambda: schedule(finalizePartition()))
mqtt.add_ready_callback(starteTick)



modules = list(filter(lambda name:name.endswith(".py"),os.listdir("scenes/")))
importnames = [ "scenes.{}".format(name[:-3]) for name in modules]
for mname in importnames:
    try:
        exec ("import {} as m\nm.register(lichtband)".format(mname))
    except Exception as e:
        print("Error while loading Module {}".format(mname))
        print (e)





# mount FS
mqtt.web.mount("/api/fs",web_filesystem.app)

def webUpdate():
    schedule(sendState())

lightWeb=LightWeb(lichtband,cb_update=webUpdate)
lightWeb.register(mqtt.web)


LOG.info("STARTING WEB APP")
# Starting main app main loop. Mqqt will manage the events and event-loop
mqtt.run()
