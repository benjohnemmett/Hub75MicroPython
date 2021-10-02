# Hub75MicroPython
Library for ESP32 MicroPython to drive an LED matrix using the Hub75 protocol.

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
