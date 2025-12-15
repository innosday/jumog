#include <iostream>
#include <atomic>
#include <csignal>
#include <thread>
#include <chrono>
#include "led.h"
#include "pir.h"
#include "ldr.h"

static std::atomic<bool> running{true};

void sigint_handler(int){ running = false; }

int main(){
    std::signal(SIGINT, sigint_handler);

    LED led(14);
    PIR pir(23);
    LDR ldr(0);
    LED onled(18);
    LED offled(15);

    bool flog = false;
    bool turnflog = false;
    int nowBright = 0;

    while(running){
        bool detected = pir.digitalRead();
        if(detected){
            if(!flog){ flog = true; turnflog = !turnflog; }
        } else {
            if(flog) flog = false;
        }

        if(turnflog){
            int raw = ldr.analogRead();
            nowBright = 100 - static_cast<int>((raw * 100) / 1023.0 + 0.5);
            led.DutyCycleWrite(nowBright);
            onled.DutyCycleWrite(100);
            offled.DutyCycleWrite(0);
        } else {
            nowBright = 0;
            led.DutyCycleWrite(0);
            onled.DutyCycleWrite(0);
            offled.DutyCycleWrite(100);
        }

        std::cout << "Detected:" << (turnflog?"Y":"N") << " Bright:" << nowBright << "\r" << std::flush;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    led.cleanup(); onled.cleanup(); offled.cleanup();
    return 0;
}
