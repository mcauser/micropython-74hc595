# SPDX-FileCopyrightText: 2021 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595
"""

__version__ = '1.0.0'

class SR74HC595_BITBANG:
    def __init__(self, ser, srclk, rclk, srclr=None, oe=None):
        self.ser = ser
        self.srclk = srclk
        self.rclk = rclk
        self.srclr = srclr  # tie high if functionality not needed
        self.oe = oe        # tie low if functionality not needed

        self.ser.init(ser.OUT, value=0)
        self.srclk.init(srclk.OUT, value=0)
        self.rclk.init(rclk.OUT, value=0)

        if self.srclr is not None:
            self.srclr.init(srclr.OUT, value=1)
        if self.oe is not None:
            self.oe.init(oe.OUT, value=0)

    def _clock(self):
        self.srclk(1)
        self.srclk(0)

    def bit(self, value, latch=False):
        self.ser(value)
        self._clock()
        if latch:
            self.latch()

    def bits(self, value, num_bits, latch=False):
        for i in range(num_bits):
            self.bit((value >> i) & 1)
        if latch:
            self.latch()

    def latch(self):
        self.rclk(1)
        self.rclk(0)

    def clear(self, latch=True):
        if self.srclr is None:
            raise RuntimeError('srclr pin is required')
        self.srclr(0)
        self.srclr(1)
        if latch:
            self.latch()

    def enable(self, enabled=True):
        if self.oe is None:
            raise RuntimeError('oe pin is required')
        self.oe(not enabled)
