# Hub75MicroPython
Library for ESP32 MicroPython to drive an LED matrix using the Hub75 protocol.

Details here -> https://notes.benjemmett.com/archives/114

## Setup
This project is based on the Hub75 Blaster PCB from this Hackerbox (https://hackerboxes.com/collections/past-hackerboxes/products/hackerbox-0065-realtime).
It can easily be reconfigured to use custom pins with the Hub75SpiConfiguration class. 

## SPI Implementation
This library uses software SPI to shift in the pixel data. It uses six separate SPI channels, two for each color, one for the top half and one for the bottom half. 
Normally with Hub75, all six channels would be shifted in simultaneously and two row would be shown at a time with three colors each.
I tried to take that approach using GPIO bitbanging, however it was too slow and the display flickered quite a bit. 
SPI is able to shift in data much quicker, however each row and color channel are illuminated individually as follows. 
1. Shift in first row red data, disable output, latch data, enable output
1. Shift in first row green data, disable output, latch data, enable output
1. Shift in first row blue data, disable output, latch data, enable output
1. Shift in second row red data, disable output, latch data, enable output
1. Shift in second row green data, disable output, latch data, enable output
1. Shift in second row blue data, disable output, latch data, enable output

...


1. Shift in last row red data, disable output, latch data, enable output
1. Shift in last row green data, disable output, latch data, enable output
1. Shift in last row blue data, disable output, latch data, enable output

The SPI approach also has drawbacks, for example the picture is a bit dim normally. 
This can be improved by increasing the illumination time on each row, however that will reduce the framerate and may cause filcker.

## Color Mapping
This library supports 3-bit color. Pixel values can be set individually with `set_pixel_value(row, col, value)` or as a group with `set_pixels(top, left, image)`. Where `value` is a bitmapped value as shown in the table below, and `image` is a 2d list of bitmapped values. 

| Color | Binary Value | Decimal Value |
|-------|--------------|--------------|
| Black   | 0b000 | 0 |
| Blue    | 0b001 | 1 |
| Green   | 0b010 | 2 |
| Cyan    | 0b011 | 3 |
| Red     | 0b100 | 4 |
| Magenta | 0b101 | 5 |
| Yellow  | 0b110 | 6 |
| White   | 0b111 | 7 |

## Example
This example displays the Python logo imported from logo.py.
````
import hub75
import matrixdata
from logo import logo

ROW_SIZE = 32
COL_SIZE = 64

config = hub75.Hub75SpiConfiguration()
matrix = matrixdata.MatrixData(ROW_SIZE, COL_SIZE)
hub75spi = hub75.Hub75Spi(matrix, config)

# Show Python Logo
matrix.set_pixels(0, 16, logo)

while True:
    hub75spi.display_data()
````

