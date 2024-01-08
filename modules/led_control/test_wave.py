#!/usr/bin/python
"""
'Wave' effect for WS2812B led strip
"""

import time

import numpy
import spidev
from numpy import sin, pi

import ws2812
from config.settings import LED_NUM


def _test_pattern_sin(_spi, num_leds=8, intensity=20):
    start_time = time.time()
    indices = 4 * numpy.array(range(num_leds), dtype=numpy.uint32) * numpy.pi / num_leds
    period0 = 2
    period1 = 2.1
    period2 = 2.2
    try:
        while True:
            _time = start_time - time.time()
            f = numpy.zeros((num_leds, 3))
            f[:, 0] = sin(2 * pi * _time / period0 + indices)
            f[:, 1] = sin(2 * pi * _time / period1 + indices)
            f[:, 2] = sin(2 * pi * _time / period2 + indices)
            f = intensity * ((f + 1.0) / 2.0)
            fi = numpy.array(f, dtype=numpy.uint8)
            ws2812.write2812(_spi, fi)
            time.sleep(0.01)
    except KeyboardInterrupt:
        ws2812.off_leds(_spi, num_leds)


if __name__ == "__main__":
    spi = spidev.SpiDev()
    spi.open(0, 0)
    _test_pattern_sin(spi, num_leds=LED_NUM, intensity=255)
