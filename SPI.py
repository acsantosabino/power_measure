
class ADC():
    #definindo um ADC
    import mraa
    bits = 12
    nchannel = 8
    buffersize = 0
    
    def __init__(self):
        self.spi = mraa.Spi(0)
        spi.frequency(1000000)
        ss=mraa.Gpio(0)
        ss.dir(mraa.DIR_OUT)
        spi.mode(mraa.SPI.MODE0)
