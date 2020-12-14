from ledcontroller import LEDController
from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout, MQTT_PREFIX, ONLINE_SUFFIX
from ledapp import LEDApp

mqtt = MQTTWebApplication(config, prefix=MQTT_PREFIX, online_suffix=ONLINE_SUFFIX, debug=True)
APP = LEDApp(mqtt)


print("STARTING WEB APP")
# Starting main app main loop. Mqqt will manage the events and event-loop
mqtt.run()
