"""
MicroPython 74HC595 8-Bit Shift Register
https://github.com/mcauser/micropython-74hc595

MIT License
Copyright (c) 2021 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '0.0.1'

class SR:
    def __init__(self, spi, rclk, len=1, srclr=None, oe=None):
        self.spi = spi
        self.rclk = rclk
        self.srclr = srclr  # tie high if functionality not needed
        self.oe = oe        # tie low if functionality not needed

        self.buf = bytearray(len)
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
            self.buf[pin // 8] |= (1 << (pin % 8))
        else:
            self.buf[pin // 8] &= ~(1 << (pin % 8))
        self._write(latch)

    def toggle(self, pin, latch=True):
        self.buf[pin // 8] ^= (1 << (pin % 8))
        self._write(latch)

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

    def __getitem__(self, index):
        return self.buf[index]

    def __setitem__(self, index, value):
        self.buf[index] = value
        self._write(True)
