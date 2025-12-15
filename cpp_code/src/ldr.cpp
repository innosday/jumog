#include "ldr.h"
#include <wiringPiSPI.h>
#include <cstring>

static bool spi_init = false;
static constexpr int SPI_CH = 0;
static constexpr int SPI_SPEED = 1350000;

LDR::LDR(int ch):channel(ch){
    if(!spi_init){
        wiringPiSPISetup(SPI_CH, SPI_SPEED);
        spi_init = true;
    }
}

LDR::~LDR() = default;

int LDR::analogRead() noexcept{
    unsigned char buf[3];
    buf[0]=1;
    buf[1]=static_cast<unsigned char>((8 + channel) << 4);
    buf[2]=0;
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    return ((buf[1] & 3) << 8) | buf[2];
}
