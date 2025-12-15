#pragma once

class PIR {
    int pin;
public:
    explicit PIR(int p);
    bool digitalRead() noexcept;
    void cleanup() noexcept;
};
