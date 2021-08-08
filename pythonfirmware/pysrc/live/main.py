from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout, MQTT_PREFIX, ONLINE_SUFFIX
from ledapp import LEDApp
from utils import create_repeat_routine
from mqttapp.utils import schedule
import uasyncio as asyncio
from testscenen import BlinkScene, RunlightScene, BlockLauflicht
from utils import LOG as UTIL_LOG

import gc

# Default Logging
import ulogging as logging
LOG = logging.getLogger(__name__)


mqtt = MQTTWebApplication(config, prefix=MQTT_PREFIX, online_suffix=ONLINE_SUFFIX, debug=True)
APP = LEDApp(mqtt)


create_repeat_routine(gc.collect, 30000)


async def starteScene1():
    await asyncio.sleep(3)
    LOG.info("STARTE SZENEN")

    ll = RunlightScene()
    farbmuster = [(200, 0, 0, 0)]*15+[(0, 0, 200, 0)]*15
    ll = BlockLauflicht(muster=farbmuster, steps_per_second=30, speed=3)
    APP.leds.add_scene(ll, region=":")
schedule(starteScene1())

UTIL_LOG.setLevel(logging.DEBUG)
LOG.info("STARTING WEB APP")
# Starting main app main loop. Mqqt will manage the events and event-loop
mqtt.run()
