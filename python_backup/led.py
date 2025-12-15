import RPi.GPIO as GPIO # type: ignore

class LED:
    def __init__(self,pin:int):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        self.pwm_led = GPIO.PWM(self.pin,500)
        self.pwm_led.start(100)
        

    def DutyCycleWrite(self,bright:int):
        self.pwm_led.ChangeDutyCycle(bright)

    def digitalWrite(self,onoff:bool):
        GPIO.output(self.pin,onoff)

    def cleanup(self):
        GPIO.cleanup(self.pin)
