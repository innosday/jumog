
from led import LED
from ldr import LDR
from pir import PIR

led = LED(18)
pir = PIR(15)
ldr = LDR(1)

def main():
    if pir.digitalRead():
        print("사람 감지됨",end=' | ')
        nowBright = ldr.analogRead()
        print("현재 밝기 : ",nowBright)
        


if __name__ == "__main__":
    main()