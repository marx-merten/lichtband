import esp32
from machine import Pin
r = esp32.RMT(0, pin=Pin(15), clock_div=4)
for i in range(10):
    r.write_pulses((5, 5, 5, 5, 10, 10, 10, 10), start=0)
