import spidev # type: ignore

class LDR:
    def __init__(self,channel):
        self.channel = channel
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi_max_speed_hz = 1350000

    def analogRead(self):
        r = self.spi.xfer2([1,(8+self.channel) << 4.0])
        abs_out = ((r[1]&3)<<8) + r[2]
        return abs_out