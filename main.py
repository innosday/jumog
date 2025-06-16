from Tkinter import AppleStyleGUI
import RPi.GPIO as GPIO # type: ignore
from led import LED
from ldr import LDR
from pir import PIR

led = LED(14)
pir = PIR(23)
ldr = LDR(0)

onled = LED(18)
offled = LED(15)
#flog = False
#turnflog = False
win = AppleStyleGUI()

flog = False
turnflog = False
nowBright = 0

def main():
    global flog
    global turnflog
    global nowBright
    try:
        if pir.digitalRead():
            if not flog:
                flog = True
                turnflog = not turnflog
        else:
            if flog:
                flog = False
        if turnflog:
            nowBright =100- round((ldr.analogRead()*100)/1023)
            #print("사람 감지됨 현재 밝기",nowBright)
            led.DutyCycleWrite(nowBright)
            onled.DutyCycleWrite(100)
            offled.DutyCycleWrite(0)
        else:
            #print("사람 감지안됨")
            nowBright = 0
            led.DutyCycleWrite(0)
            onled.DutyCycleWrite(0)
            offled.DutyCycleWrite(100)
        win.update_ui(turnflog, nowBright)
        win.after(100,main)
    except:
        GPIO.cleanup()
        win.destory()


if __name__ == "__main__":
    win.protocol("closed win",lambda: (led.cleanup(),onled.cleanup(),offled.cleanup(),pir.cleanup(),win.destory()))
    win.after(100,main)
    win.mainloop()

