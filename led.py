import RPi.GPIO as GPIO  # type: ignore
import time

class LED:
    def __init__(self,pin:int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)

    def DutyCycleWrite(self,bright:int,delay:int):
        """
        Args:
            bright: %
            delay: ms
        """
        for _ in range(delay//10):
            GPIO.output(self.pin,True)
            time.sleep(bright//10)
            GPIO.output(self.pin,False)
            time.sleep(10-bright//10)

    def cleanup(self):
        GPIO.cleanup(self.pin)