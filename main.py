
from led import LED
from ldr import LDR
from pir import PIR

led = LED(15)
pir = PIR(18)
ldr = LDR(0)

def main():
    try:
        while True:
            if not pir.digitalRead():
                print("사람 감지됨",end=' | ')
                nowBright = ldr.analogRead()
                print("현재 밝기 : ",nowBright)
                if nowBright >=600:
                    led.DutyCycleWrite(0)
                elif nowBright >=400:
                    led.DutyCycleWrite(60)
                elif nowBright>=200:
                    led.DutyCycleWrite(80)
            else:
                print("감지 안됨")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
    led.cleanup()
    pir.cleanup()
