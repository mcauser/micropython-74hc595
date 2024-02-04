# SPDX-FileCopyrightText: 2021 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595
"""

from machine import Pin, SPI
from sr74hc595 import SR74HC595_SPI

spi = SPI(1, 100000)
rclk = Pin(5, Pin.OUT)

oe = Pin(33, Pin.OUT, value=0)  # low enables output
srclr = Pin(32, Pin.OUT, value=1)  # pulsing low clears data

sr = SR74HC595_SPI(spi, rclk, 2)  # chain of 2 shift registers

sr.pin(2, 1)  # set pin 2 high of furthest shift register
sr.pin(2)  # read pin 2
sr.pin(2, 0)  # set pin 2 low

sr.toggle(8)  # toggle first pin of closest shift register

sr[0] = 0xFF  # set all pins high on furthest shift register
sr[1] = 240  # set half pins high on closest shift register
print(sr[1])  # read pins

oe.value(0)  # disable outputs
oe.value(1)  # enable outputs

# pulse to clear shift register memory
srclr.value(1)
srclr.value(0)
