from tkinter import *
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
win = Tk()
win.title("맞춤 조명")
win.geometry('200x100')
win.resizable(width = True,height = True)

Sensor = Label(win,text="감지 안됨",bg="#fff000",font=('',20),padx=5)

Bright = Label(win,text="OFF",font=('',15))

Sensor.pack()
Bright.pack()


def setSensor(replace):
    Sensor.config(text=replace)

def setBright(bright):
    Bright.config(text=bright)
flog = False
turnflog = False

def main():
    global flog
    global turnflog
    try:
        if pir.digitalRead():
            if not flog:
                flog = True
                turnflog = not turnflog
        else:
            if flog:
                flog = False
        if turnflog:
            setSensor("감지")
            print("사람 감지됨",end=' | ')
            nowBright =100- round((ldr.analogRead()*100)/1023)
            setBright(f"현재 밝기 : {nowBright}")
            print("현재 밝기",nowBright)
            led.DutyCycleWrite(nowBright)
            onled.DutyCycleWrite(100)
            offled.DutyCycleWrite(0)
        else:
            setSensor("감지안됨")
            print("사람 감지안됨")
            setBright("OFF")
            led.DutyCycleWrite(0)
            onled.DutyCycleWrite(0)
            offled.DutyCycleWrite(100)
        win.after(100,main)
    except:
        GPIO.cleanup()
        win.destory()


if __name__ == "__main__":
    win.protocol("closed win",lambda: (led.cleanup(),onled.cleanup(),offled.cleanup(),pir.cleanup(),win.destory()))
    win.after(100,main)
    win.mainloop()

