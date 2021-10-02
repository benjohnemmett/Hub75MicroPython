from machine import Pin, SoftSPI, freq
from time import sleep_us

freq(240000000)

class Hub75SpiConfiguration:

    def __init__(self):
        self.MatrixRows = 32
        self.HalfMatrixRows = 16
        self.MatrixColumns = 64

        self.SpiMisoPinNumber = 13
        self.SpiBaudRate = 2500000
        
        self.IlluminationTimeMicroseconds = 10

        # Row select pins
        self.LineSelectAPinNumber = 5
        self.LineSelectBPinNumber = 18
        self.LineSelectCPinNumber = 19
        self.LineSelectDPinNumber = 21
        self.LineSelectEPinNumber = 12

        # Hub75 RGB data pins
        self.Red1PinNumber = 2
        self.Blue1PinNumber = 15
        self.Green1PinNumber = 4
        self.Red2PinNumber = 16
        self.Blue2PinNumber = 27
        self.Green2PinNumber = 17

        self.ClockPinNumber = 22
        self.LatchPinNumber = 26
        self.OutputEnablePinNumber = 25 # active low


class Hub75Spi:

    def __init__(self, config):
        self.config = config

        self.LatchPin = Pin(config.LatchPinNumber, Pin.OUT)
        self.OutputEnablePin = Pin(config.OutputEnablePinNumber, Pin.OUT)
        self.LineSelectAPin = Pin(config.LineSelectAPinNumber, Pin.OUT)
        self.LineSelectBPin = Pin(config.LineSelectBPinNumber, Pin.OUT)
        self.LineSelectCPin = Pin(config.LineSelectCPinNumber, Pin.OUT)
        self.LineSelectDPin = Pin(config.LineSelectDPinNumber, Pin.OUT)
        self.LineSelectEPin = Pin(config.LineSelectEPinNumber, Pin.OUT)

        self.LineSelectAPin.off()
        self.LineSelectBPin.off()
        self.LineSelectCPin.off()
        self.LineSelectDPin.off()
        self.LineSelectEPin.off()
        
        self.Red1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Red1PinNumber), miso=Pin(config.SpiMisoPinNumber))
        self.Red2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Red2PinNumber), miso=Pin(config.SpiMisoPinNumber))
        self.Green1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Green1PinNumber), miso=Pin(config.SpiMisoPinNumber))
        self.Green2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Green2PinNumber), miso=Pin(config.SpiMisoPinNumber))
        self.Blue1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Blue1PinNumber), miso=Pin(config.SpiMisoPinNumber))
        self.Blue2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=Pin(config.Blue2PinNumber), miso=Pin(config.SpiMisoPinNumber))

        self.RedMatrixData = [bytearray(8) for x in range(32)]
        self.GreenMatrixData = [bytearray(8) for x in range(32)]
        self.BlueMatrixData = [bytearray(8) for x in range(32)]
        
        self.DirtyBytesArray = []
        
        
    def SetRowSelect(self, row):
        self.LineSelectAPin.value(row & 1)
        self.LineSelectBPin.value(row & 2)
        self.LineSelectCPin.value(row & 4)
        self.LineSelectDPin.value(row & 8)
        self.LineSelectEPin.value(row & 16)


    def DisplayTopHalf(self):
        for row in range(self.config.HalfMatrixRows):
            # shift in data
            RowData = self.RedMatrixData[row]
            self.Red1Spi.write(RowData)
            self.OutputEnablePin.on() # disable

            self.SetRowSelect(row)

            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            # shift in data
            RowData = self.GreenMatrixData[row]
            self.Green1Spi.write(RowData)
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            # shift in data
            RowData = self.BlueMatrixData[row]
            self.Blue1Spi.write(RowData)
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
        self.Blue1Spi.write(bytearray(8))


    def DisplayBottomHalf(self):
        for row in range(self.config.HalfMatrixRows, self.config.MatrixRows):
            # shift in data
            RowData = self.RedMatrixData[row]
            self.Red2Spi.write(RowData)
            self.OutputEnablePin.on() # disable

            self.SetRowSelect(row % self.config.HalfMatrixRows)

            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            RowData = self.GreenMatrixData[row]
            self.Green2Spi.write(RowData)
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
                        
            RowData = self.BlueMatrixData[row]
            self.Blue2Spi.write(RowData)
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)

        self.Blue2Spi.write(bytearray(8))


    def DisplayData(self):
        self.DisplayTopHalf()
        self.DisplayBottomHalf()
        

    def SetPixelValue(self, row, col, val):
        if (self.IsOutOfBounds(row, col)):
            return
        
        cIndex = col // 8
        byteIndex = 7 - (col % 8)

        if val & 4:
            self.RedMatrixData[row][cIndex] |= (1 << byteIndex)
        if val & 2:
            self.GreenMatrixData[row][cIndex] |= (1 << byteIndex)
        if val & 1:
            self.BlueMatrixData[row][cIndex] |= (1 << byteIndex)
        
        self.DirtyBytesArray.append((row,col//8))
    

    def ClearDirtyBytes(self):
        for index in self.DirtyBytesArray:
            self.RedMatrixData[index[0]][index[1]] = 0
            self.GreenMatrixData[index[0]][index[1]] = 0
            self.BlueMatrixData[index[0]][index[1]] = 0
            
        self.DirtyBytesArray = []
    

    def SetPixels(self, row, col, array):
        for r in range(len(array)):
            for c in range(len(array[0])):
                if array[r][c]:
                    self.SetPixelValue(row + r, col + c, array[r][c])
    

    def IsOutOfBounds(self, row, col):
        return (row < 0 or row >= self.config.MatrixRows or col < 0 or col >= self.config.MatrixColumns)

