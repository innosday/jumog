#pragma once

class LED {
    int pin;
    bool hardwarePWM;
public:
    explicit LED(int p);
    void DutyCycleWrite(int percent) noexcept;
    void digitalWrite(bool on) noexcept;
    void cleanup() noexcept;
};
