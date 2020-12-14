from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout


class LEDApp:
    def __init__(self, app: MQTTWebApplication):
        self.leds = LEDController(pinout.PIN_LED1, bpp=4, pixel=60)
        app.subscribe('licht', self.licht)

    async def licht(self, topic, msg, retain):
        print("LICHT: {}  -> {}".format(topic, msg))
