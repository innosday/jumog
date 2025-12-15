#include "led.h"
#include <wiringPi.h>
#include <softPwm.h>
#include <wiringPiSPI.h>
#include <unistd.h>

LED::LED(int p):pin(p),hardwarePWM(false){
    wiringPiSetupGpio();
    pinMode(pin, OUTPUT);
    if(pin == 18){
        hardwarePWM = true;
        pwmSetMode(PWM_MODE_MS);
        pwmSetRange(1024);
        pwmSetClock(384);
        pwmWrite(pin, 1024);
    } else {
        softPwmCreate(pin, 100, 100);
        softPwmWrite(pin, 100);
    }
}

void LED::DutyCycleWrite(int percent) noexcept{
    if(percent < 0) percent = 0;
    if(percent > 100) percent = 100;
    if(hardwarePWM){
        int val = (percent * 1023) / 100;
        pwmWrite(pin, val);
    } else {
        softPwmWrite(pin, percent);
    }
}

void LED::digitalWrite(bool on) noexcept{
    ::digitalWrite(pin, on ? HIGH : LOW);
}

void LED::cleanup() noexcept{
    if(hardwarePWM){
        pwmWrite(pin, 0);
    } else {
        softPwmWrite(pin, 0);
    }
}
