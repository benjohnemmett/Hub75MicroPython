from machine import Pin, SoftSPI, freq
from time import sleep_us
from matrixdata import MatrixData

freq(240000000)

class Hub75SpiConfiguration:

    def __init__(self):
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

    def __init__(self, matrix_data, config):
        self.config = config

        self.matrix_data = matrix_data
        self.half_row_size = matrix_data.row_size //2

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

        self.red1_mosi_pin = Pin(config.Red1PinNumber)
        self.red2_mosi_pin = Pin(config.Red2PinNumber)
        self.green1_mosi_pin = Pin(config.Green1PinNumber)
        self.green2_mosi_pin = Pin(config.Green2PinNumber)
        self.blue1_mosi_pin = Pin(config.Blue1PinNumber)
        self.blue2_mosi_pin = Pin(config.Blue2PinNumber)
        
        self.Red1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.red1_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        self.Red2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.red2_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        self.Green1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.green1_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        self.Green2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.green2_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        self.Blue1Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.blue1_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        self.Blue2Spi = SoftSPI(baudrate=config.SpiBaudRate, polarity=1, phase=0, sck=Pin(config.ClockPinNumber), mosi=self.blue2_mosi_pin, miso=Pin(config.SpiMisoPinNumber))
        
    def SetRowSelect(self, row):
        self.LineSelectAPin.value(row & 1)
        self.LineSelectBPin.value(row & 2)
        self.LineSelectCPin.value(row & 4)
        self.LineSelectDPin.value(row & 8)
        self.LineSelectEPin.value(row & 16)

    def DisplayTopHalf(self):
        for row in range(self.half_row_size):
            # shift in data
            RowData = self.matrix_data.red_matrix_data[row]
            self.Red1Spi.write(RowData)
            self.red1_mosi_pin.off()
            self.OutputEnablePin.on() # disable

            self.SetRowSelect(row)

            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            # shift in data
            RowData = self.matrix_data.green_matrix_data[row]
            self.Green1Spi.write(RowData)
            self.green1_mosi_pin.off()
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            # shift in data
            RowData = self.matrix_data.blue_matrix_data[row]
            self.Blue1Spi.write(RowData)
            self.blue1_mosi_pin.off()
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)

    def DisplayBottomHalf(self):
        for row in range(self.half_row_size, self.matrix_data.row_size):
            # shift in data
            RowData = self.matrix_data.red_matrix_data[row]
            self.Red2Spi.write(RowData)
            self.red2_mosi_pin.off()
            self.OutputEnablePin.on() # disable

            self.SetRowSelect(row % self.half_row_size)

            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
            
            RowData = self.matrix_data.green_matrix_data[row]
            self.Green2Spi.write(RowData)
            self.green2_mosi_pin.off()
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)
                        
            RowData = self.matrix_data.blue_matrix_data[row]
            self.Blue2Spi.write(RowData)
            self.blue2_mosi_pin.off()
            self.OutputEnablePin.on() # disable
            self.LatchPin.on()
            self.LatchPin.off()
            self.OutputEnablePin.off() # enable
            sleep_us(self.config.IlluminationTimeMicroseconds)

    def DisplayData(self):
        self.DisplayTopHalf()
        self.DisplayBottomHalf()
        
