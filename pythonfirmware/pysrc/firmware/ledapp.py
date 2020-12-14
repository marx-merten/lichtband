from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout
from mqttapp.utils import schedule


class LEDApp:
    def __init__(self, app: MQTTWebApplication):
        self.leds = LEDController(pinout.PIN_LED1, bpp=4, pixel=60)
        app.subscribe('licht/', self.licht)
        self.app = app
        self.rgbw = (0, 0, 0, 0xff)
        self.state = False

    def update(self):
        if not self.state:
            self.leds.fill((0, 0, 0, 0))
        else:
            self.leds.fill(self.rgbw)

    async def licht(self, fullTopic, topic, msg, retain):
        print("LICHT: {}  -> {}".format(topic, msg))
        cmds = topic.split('/')
        if (len(cmds) > 1):
            verb = cmds[0]
            command = cmds[1] == 'set'
        else:
            verb = cmds[0]
            command = False
        if command:
            if verb == "state":
                self.state = msg == 'true'
                self.update()
                if command:
                    t = fullTopic[1:-len('/set')]
                    schedule(self.app.publish(t, msg))

            if verb == "rgbw":
                b = int(msg)
                (r, g, b, w) = (b >> 24, b >> 16 & 0xff, b >> 8 & 0xff, b & 0xff)
                self.rgbw = (r, g, b, w)
                self.update()
                if command:
                    t = fullTopic[1:-len('/set')]
                    schedule(self.app.publish(t, msg))
