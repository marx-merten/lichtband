from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout
from mqttapp.utils import schedule
import uasyncio as asyncio
from machine import Pin

# Default Logging
import ulogging as logging
LOG = logging.getLogger(__name__)


class LEDApp:
    def __init__(self, app: MQTTWebApplication):
        self.leds = LEDController(pinout.PIN_LED1, bpp=4, pixel=300, tick_cb=self.tick_cb, fps=20)
        app.subscribe('licht/', self.licht)
        self.app = app
        self.rgbw = (0, 0, 0, 0xff)
        self.state = False
        self.recovery = True
        app.add_ready_callback(lambda: schedule(self._delay_recovery_end(20)))
        self.busy = asyncio.Lock()
        self.diag = Pin(pinout.PIN_DEBUG, Pin.OUT)
        self.diag2 = Pin(pinout.PIN_DEBUG2, Pin.OUT)

    def tick_cb(self, frame, finalDelay=0):
        if frame % 2 == 0:
            self.diag.off()
        else:
            self.diag.on()
        if finalDelay < 0:
            self.diag2.on()
        else:
            self.diag2.off()

    def update(self):
        if not self.state:
            self.leds.base_color = (0, 0, 0, 0)
        else:
            self.leds.base_color = self.rgbw

    def _end_recovery(self):
        if self.recovery:
            self.recovery = False
            LOG.info("Ending recovery period ended.")

    async def _delay_recovery_end(self, delay):
        LOG.info("Ending recovery period in {} seconds".format(delay))
        await asyncio.sleep(delay)
        self._end_recovery()

    async def licht(self, fullTopic, topic, msg, retain):
        LOG.debug("LICHT: {}  -> {}".format(topic, msg))

        cmds = topic.split('/')
        if (len(cmds) > 1):
            verb = cmds[0]
            command = cmds[1] == 'set'
        else:
            verb = cmds[0]
            command = False
        if command or self.recovery:
            if verb == "state":
                self.state = msg == 'true'
                self.update()
                if command:
                    self._end_recovery()
                    t = fullTopic[1:-len('/set')]
                    await self.app.publish(t, msg)

            if verb == "rgbw":
                b = int(msg)
                (r, g, b, w) = (b >> 24, b >> 16 & 0xff, b >> 8 & 0xff, b & 0xff)
                # TODO: Evtl need to find a delay value and go for last value seen
                self.rgbw = (r, g, b, w)
                self.update()
                if command:
                    self._end_recovery()
                    t = fullTopic[1:-len('/set')]
                    await self.app.publish(t, msg)
