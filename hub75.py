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
        self.B1 = 15
        self.G1 = 4
        self.R2 = 16
        self.B2 = 27
        self.G2 = 17

        self.CLK = 22
        self.LAT = 26
        self.OE = 25 # active low

        self.COLS = 64
        self.ROWS = 32
        self.HALF_ROWS = 16

        # not really used. Shared for top & bottom half of matrix.
        self.miso = 13
        self.spiBaudRate = 1000000
        
        self.illuminationTimeMicroseconds = 0


class Hub75Spi:

    def __init__(self, config):
        self.config = config

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
        
        self.spiR1 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.R1), miso=Pin(config.miso))
        self.spiR2 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.R2), miso=Pin(config.miso))
        self.spiG1 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.G1), miso=Pin(config.miso))
        self.spiG2 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.G2), miso=Pin(config.miso))
        self.spiB1 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.B1), miso=Pin(config.miso))
        self.spiB2 = SoftSPI(baudrate=config.spiBaudRate, polarity=1, phase=0, sck=Pin(config.CLK), mosi=Pin(config.B2), miso=Pin(config.miso))

        self.redData = [bytearray(8) for x in range(32)]
        self.greenData = [bytearray(8) for x in range(32)]
        self.blueData = [bytearray(8) for x in range(32)]
        
        self.dirtyBytes = {}
        
        
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
            buf = self.redData[row]
            self.spiR1.write(buf)
            self.pOe.on() # disable

            self.SetRowSelect(row)

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)
            
            # shift in data
            buf = self.greenData[row]
            self.spiG1.write(buf)
            self.pOe.on() # disable

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)
            
            # shift in data
            buf = self.blueData[row]
            self.spiB1.write(buf)
            self.pOe.on() # disable

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)
            
            
        self.spiB1.write(bytearray(8))


    def DisplayBottomHalf(self):
        for row in range(self.config.HALF_ROWS, self.config.ROWS):
            # shift in data
            buf = self.redData[row]
            self.spiR2.write(buf)
            self.pOe.on() # disable

            self.SetRowSelect(row % self.config.HALF_ROWS)

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)
            
            buf = self.greenData[row]
            self.spiG2.write(buf)
            self.pOe.on() # disable

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)
                        
            buf = self.blueData[row]
            self.spiB2.write(buf)
            self.pOe.on() # disable

            self.pLat.on()
            self.pLat.off()
            self.pOe.off() # enable
            time.sleep_us(self.config.illuminationTimeMicroseconds)

        self.spiB2.write(bytearray(8))


    def DisplayData(self):
        self.DisplayTopHalf()
        self.DisplayBottomHalf()
        

    def SetPixelValue(self, row, col, val):
        if (self.IsOutOfBounds(row, col)):
            return
        
        cIndex = col // 8
        byteIndex = 7 - (col % 8)

        if val & 4:
            self.redData[row][cIndex] |= (1 << byteIndex)
        if val & 2:
            self.greenData[row][cIndex] |= (1 << byteIndex)
        if val & 1:
            self.blueData[row][cIndex] |= (1 << byteIndex)
        
        self.dirtyBytes[(row,col//8)] = 1
    
    def ClearDirtyBytes(self):
        for index in self.dirtyBytes:
            self.redData[index[0]][index[1]] = 0
            self.greenData[index[0]][index[1]] = 0
            self.blueData[index[0]][index[1]] = 0
            
        self.dirtyBytes = {}
    
    def SetPixels(self, row, col, array):
        for r in range(len(array)):
            for c in range(len(array[0])):
                if array[r][c]:
                    self.SetPixelValue(row + r, col + c, array[r][c])
    
    def IsOutOfBounds(self, row, col):
        return (row < 0 or row >= self.config.ROWS or col < 0 or col >= self.config.COLS)
