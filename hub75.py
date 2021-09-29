from machine import Pin, SoftSPI
import time

class Hub75SpiConfiguration:

    def __init__(self):
        self.ROWS = 32
        self.HALF_ROWS = 16
        self.COLS = 64

        self.A = 5
        self.B = 18
        self.C = 19
        self.D = 21
        self.E = 12

        self.R1 = 2
        self.G1 = 15
        self.B1 = 4
        self.R2 = 16
        self.G2 = 27
        self.B2 = 17

        self.CLK = 22
        self.LAT = 26
        self.OE = 25 # active low

        self.COLS = 64
        self.ROWS = 32
        self.HALF_ROWS = 16

        # not really used. Shared for top & bottom half of matrix.
        self.miso = 13 

class Hub75Spi:

    def __init__(self, config):
        self.config = config
        #pR1 = Pin(R1, Pin.OUT, value=0)
        self.pG1 = Pin(config.G1, Pin.OUT, value=0)
        self.pB1 = Pin(config.B1, Pin.OUT, value=0)
        self.pR2 = Pin(config.R2, Pin.OUT, value=0)
        self.pG2 = Pin(config.G2, Pin.OUT, value=0)
        self.pB2 = Pin(config.B2, Pin.OUT, value=0)

        self.pLat = Pin(config.LAT, Pin.OUT)
        self.pOe = Pin(config.OE, Pin.OUT)
        self.pA = Pin(config.A, Pin.OUT)
        self.pB = Pin(config.B, Pin.OUT)
        self.pC = Pin(config.C, Pin.OUT)
        self.pD = Pin(config.D, Pin.OUT)
        self.pE = Pin(config.E, Pin.OUT)

        self.pA.off()
        self.pB.off()
        self.pC.off()
        self.pD.off()
        self.pE.off()

        self.spiR1 = SoftSPI(baudrate=1000000, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.R1), miso=Pin(config.miso))
        self.spiR2 = SoftSPI(baudrate=1000000, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.R2), miso=Pin(config.miso))

        self.data = [bytearray(8) for x in range(32)]

    def SetRowSelect(self, row):
        if row & 1:
            self.pA.on()
        else:
            self.pA.off()
        if row & 2:
            self.pB.on()
        else:
            self.pB.off()
        if row & 4:
            self.pC.on()
        else:
            self.pC.off()
        if row & 8:
            self.pD.on()
        else:
            self.pD.off()
        if row & 16:
            self.pE.on()
        else:
            self.pE.off()

    def DisplayTopHalf(self):
        for row in range(self.config.HALF_ROWS):
            # shift in data
            buf = self.data[row]
            self.spiR1.write(buf)
            self.pOe.on() # disable

            self.SetRowSelect(row)

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            
        self.spiR1.write(bytearray(8))

    def DisplayBottomHalf(self):
        for row in range(self.config.HALF_ROWS, self.config.ROWS):
            # shift in data
            buf = self.data[row]
            self.spiR2.write(buf)
            self.pOe.on() # disable

            self.SetRowSelect(row % self.config.HALF_ROWS)

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable

        self.spiR2.write(bytearray(8))

    def DisplayData(self):
        self.DisplayTopHalf()
        self.DisplayBottomHalf()

    def SetPixelValue(self, row, col):
        cIndex = col // 8
        byteIndex = 7 - (col % 8)

        self.data[row][cIndex] |= (1 << byteIndex)
    
    def ClearPixelValue(self, row, col):
        cIndex = col // 8
        byteIndex = 7 - (col % 8)

        self.data[row][cIndex] &= ~(1 << byteIndex)

