# SPDX-FileCopyrightText: 2021 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595
"""

from machine import Pin
from sr74hc595 import SR74HC595_BITBANG

ser = Pin(23, Pin.OUT)
rclk = Pin(5, Pin.OUT)
srclk = Pin(18, Pin.OUT)

# construct without optional pins
sr = SR74HC595_BITBANG(ser, srclk, rclk)

sr.clear()  # raises RuntimeError because you haven't provide srclr pin
sr.enable()  # raises RuntimeError because you haven't provide oe pin

# reconstruct with all pins
oe = Pin(33, Pin.OUT, value=0)  # low enables output
srclr = Pin(32, Pin.OUT, value=1)  # pulsing low clears data

sr = SR74HC595_BITBANG(ser, srclk, rclk, srclr, oe)

sr.bit(1)  # send high bit, do not latch yet
sr.bit(0)  # send low bit, do not latch yet
sr.latch()  # latch outputs, outputs=0000_0010

sr.bit(1, 1)  # send high bit and latch, outputs=0000_0101
sr.bit(0, 1)  # send low bit and latch, outputs=0000_1010

sr.bits(0xFF, 4)  # send 4 lowest bits of 0xff (sends 0x0f), outputs=1010_1111

sr.clear(0)  # clear the memory but don't latch yet
sr.latch()  # next latch shows the outputs have been reset

sr.bits(0b1010_1010, 8)  # write some bits
sr.clear()  # clear the memory and latch, outputs have been reset

sr.enable()  # outputs enabled
sr.enable(0)  # outputs disabled
