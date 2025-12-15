#pragma once
#include <cstdint>

class LDR {
    int channel;
public:
    explicit LDR(int ch);
    ~LDR();
    int analogRead() noexcept;
};
