from mqttapp import MQTTApplication, MQTTWebApplication
from config import config, pinout

APP = MQTTWebApplication(config, prefix=config['prefix'], online_suffix='device/connect', debug=True)
print("STARTING WEB APP")
APP.run()
