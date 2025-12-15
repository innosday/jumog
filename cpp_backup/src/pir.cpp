#include "pir.h"
#include <wiringPi.h>

PIR::PIR(int p):pin(p){
    wiringPiSetupGpio();
    pinMode(pin, INPUT);
}

bool PIR::digitalRead() noexcept{
    return ::digitalRead(pin) != 0;
}

void PIR::cleanup() noexcept{
}
