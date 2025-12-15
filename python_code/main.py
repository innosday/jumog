from gui import AppleStyleGUI
import RPi.GPIO as GPIO # type: ignore
from led import LED
from ldr import LDR
from pir import PIR

led = LED(14)
pir = PIR(23)
ldr = LDR(0)

onled = LED(18)
offled = LED(15)
win = AppleStyleGUI()

# state machine
STATE_IDLE = 0
STATE_ACTIVE = 1
STATE_ADJUST = 2

turnflog = False
prev_pir = pir.digitalRead()

# moving average buffer
MA_SIZE = 10
samples = [0] * MA_SIZE
sample_idx = 0
sample_count = 0
sample_sum = 0

target_duty = 0
current_duty = 0
MAX_STEP = 5
state = STATE_IDLE

def main():
    global turnflog, prev_pir
    global samples, sample_idx, sample_count, sample_sum
    global target_duty, current_duty, state
    try:
        pir_val = pir.digitalRead()
        # rising edge toggle
        if pir_val and not prev_pir:
            turnflog = not turnflog
            state = STATE_ACTIVE if turnflog else STATE_IDLE
        prev_pir = pir_val

        # read sensor and update moving average
        new_raw = ldr.analogRead()
        sample_sum -= samples[sample_idx]
        samples[sample_idx] = new_raw
        sample_sum += new_raw
        sample_idx = (sample_idx + 1) % MA_SIZE
        if sample_count < MA_SIZE:
            sample_count += 1
        avg_raw = sample_sum // (sample_count if sample_count else 1)

        if state == STATE_IDLE:
            target_duty = 0
        elif state == STATE_ACTIVE:
            target_duty = 100 - round((avg_raw * 100) / 1023)
            state = STATE_ADJUST
        else:  # ADJUST
            target_duty = 100 - round((avg_raw * 100) / 1023)

        # smooth dimming
        if current_duty < target_duty:
            current_duty = min(current_duty + MAX_STEP, target_duty)
        elif current_duty > target_duty:
            current_duty = max(current_duty - MAX_STEP, target_duty)

        led.DutyCycleWrite(current_duty)
        if turnflog:
            onled.DutyCycleWrite(100)
            offled.DutyCycleWrite(0)
        else:
            onled.DutyCycleWrite(0)
            offled.DutyCycleWrite(100)

        win.update_ui(turnflog, current_duty)
        win.after(100, main)
    except Exception:
        GPIO.cleanup()
        win.destory()


if __name__ == "__main__":
    win.protocol("closed win",lambda: (led.cleanup(),onled.cleanup(),offled.cleanup(),pir.cleanup(),win.destory()))
    win.after(100,main)
    win.mainloop()
