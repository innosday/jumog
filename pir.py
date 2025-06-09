import RPi.GPIO as GPIO # type: ignore

class PIR:
    def __init__(self,pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.IN)
    
    def digitalRead(self) -> bool:
        return GPIO.input(self.pin)
    
    def cleanup(self):
        GPIO.cleanup(self.pin)