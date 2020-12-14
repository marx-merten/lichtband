from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout
from ledapp import LEDApp

mqtt = MQTTWebApplication(config, prefix=config['prefix'], online_suffix='device/connect', debug=True)
APP = LEDApp(mqtt)


print("STARTING WEB APP")
# Starting main app main loop. Mqqt will manage the events and event-loop
mqtt.run()
