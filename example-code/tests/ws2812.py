#!/usr/bin/env python3

# This program must be executed with root privileges.
# Enter the command:
# sudo ./ws2812.py

import time

import board
import neopixel

from config import *  # pylint: disable=unused-wildcard-import


def test():
    print('\nWS2812 test.')
    pixels = neopixel.NeoPixel(
        board.D18, 8, brightness=1.0/32, auto_write=False)

    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)

    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)

    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(1)

    pixels[0] = (255, 0, 0)
    pixels[1] = (0, 255, 0)
    pixels[2] = (0, 0, 255)
    pixels[3] = (255, 0, 0)
    pixels[4] = (0, 255, 0)
    pixels[5] = (0, 0, 255)
    pixels[6] = (0, 255, 255)
    pixels[7] = (255, 0, 255)
    pixels.show()
    time.sleep(1)

    pixels.fill((255, 255, 255))
    pixels.show()
    time.sleep(1)

    pixels.fill((0, 0, 0))
    pixels.show()


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member
