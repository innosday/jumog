from ldr import LDR
from pir import PIR
from led import LED
import time
ldr = LDR(0)
pir = PIR(18)
led = LED(15)

try:
    while True:
        led.DutyCycleWrite(80)
        print(ldr.analogRead(),pir.digitalRead())
        time.sleep(1)
        led.DutyCycleWrite(20)
        time.sleep(1)
except KeyboardInterrupt:
    pass

