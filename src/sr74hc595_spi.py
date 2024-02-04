# SPDX-FileCopyrightText: 2021 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595
"""

__version__ = "1.0.1"


class SR74HC595_SPI:
    def __init__(self, spi, rclk, length=1, srclr=None, oe=None):
        self.spi = spi
        self.rclk = rclk
        self.srclr = srclr  # tie high if functionality not needed
        self.oe = oe  # tie low if functionality not needed

        self.buf = bytearray(length)
        self.rclk.init(rclk.OUT, value=0)

        if self.srclr is not None:
            self.srclr.init(srclr.OUT, value=1)
        if self.oe is not None:
            self.oe.init(oe.OUT, value=0)

    def _write(self, latch=False):
        self.spi.write(self.buf)
        if latch:
            self.latch()

    def latch(self):
        self.rclk(1)
        self.rclk(0)

    def pin(self, pin, value=None, latch=True):
        if value is None:
            return (self.buf[pin // 8] >> (pin % 8)) & 1
        elif value:
            self.buf[pin // 8] |= 1 << (pin % 8)
        else:
            self.buf[pin // 8] &= ~(1 << (pin % 8))
        self._write(latch)

    def toggle(self, pin, latch=True):
        self.buf[pin // 8] ^= 1 << (pin % 8)
        self._write(latch)

    def clear(self, latch=True):
        if self.srclr is None:
            raise RuntimeError("srclr pin is required")
        self.srclr(0)
        self.srclr(1)
        if latch:
            self.latch()

    def enable(self, enabled=True):
        if self.oe is None:
            raise RuntimeError("oe pin is required")
        self.oe(not enabled)

    def __getitem__(self, index):
        return self.buf[index]

    def __setitem__(self, index, value):
        self.buf[index] = value
        self._write(True)
