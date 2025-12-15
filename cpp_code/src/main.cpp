#include <iostream>
#include <atomic>
#include <csignal>
#include <thread>
#include <chrono>
#include <cmath>
#include "led.h"
#include "pir.h"
#include "ldr.h"

static std::atomic<bool> running{true};

void sigint_handler(int){ running = false; }

enum class State { IDLE, ACTIVE, ADJUST };

int main(){
    std::signal(SIGINT, sigint_handler);

    LED led(14);
    PIR pir(23);
    LDR ldr(0);
    LED onled(18);
    LED offled(15);

    State state = State::IDLE;
    bool turnflog = false;
    bool prevPir = pir.digitalRead();

    int targetDuty = 0;
    int currentDuty = 0;
    const int maxStep = 5; // percent per 100ms

    constexpr int MA_SIZE = 10;
    int samples[MA_SIZE] = {0};
    int sampleIdx = 0;
    int sampleCount = 0;
    int sampleSum = 0;

    while(running){
        bool pirVal = pir.digitalRead();
        if(pirVal && !prevPir){ // rising edge
            turnflog = !turnflog;
            state = turnflog ? State::ACTIVE : State::IDLE;
        }
        prevPir = pirVal;

        // read sensor and update moving average
        int newRaw = ldr.analogRead();
        sampleSum -= samples[sampleIdx];
        samples[sampleIdx] = newRaw;
        sampleSum += newRaw;
        sampleIdx = (sampleIdx + 1) % MA_SIZE;
        if(sampleCount < MA_SIZE) ++sampleCount;
        int avgRaw = sampleSum / (sampleCount ? sampleCount : 1);

        if(state == State::IDLE){
            targetDuty = 0;
        } else if(state == State::ACTIVE){
            targetDuty = 100 - static_cast<int>(std::round((avgRaw * 100.0) / 1023.0));
            state = State::ADJUST;
        } else { // ADJUST
            targetDuty = 100 - static_cast<int>(std::round((avgRaw * 100.0) / 1023.0));
        }

        // smooth step towards target
        if(currentDuty < targetDuty) currentDuty = std::min(currentDuty + maxStep, targetDuty);
        else if(currentDuty > targetDuty) currentDuty = std::max(currentDuty - maxStep, targetDuty);

        led.DutyCycleWrite(currentDuty);
        if(turnflog){ onled.DutyCycleWrite(100); offled.DutyCycleWrite(0); }
        else { onled.DutyCycleWrite(0); offled.DutyCycleWrite(100); }

        std::cout << "State:" << (state==State::IDLE?"IDLE":(state==State::ACTIVE?"ACTIVE":"ADJUST"))
                  << " Turn:" << (turnflog?"Y":"N") << " Duty:" << currentDuty << "\r" << std::flush;

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    led.cleanup(); onled.cleanup(); offled.cleanup();
    return 0;
}
