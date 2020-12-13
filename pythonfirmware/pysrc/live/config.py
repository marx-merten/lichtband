# config.py Local configuration for mqtt_as demo programs.
from sys import platform
from mqtt_as import config
import globals.pinout as pinout


# Not needed if you're only using ESP8266
#        wlan.connect("mwThings", 'S3cretThingz')

config['ssid'] = 'mwThings'
config['wifi_pw'] = 'S3cretThingz'

config['server'] = '172.17.0.46'
config['port'] = 9883
config['prefix'] = "iot/0/benjamin/lichtleiste/0/"
config['leds'] = 300
