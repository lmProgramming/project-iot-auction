#!/usr/bin/env python3
# This program must be executed with root privileges.
# Enter the command:
# sudo ./ws2812.py
import time
import os
import board
import neopixel
from config import *

def test():
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.5)

    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)

    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(0.5)

    pixels[0] = (255, 0, 0)
    pixels[1] = (0, 255, 0)
    pixels[2] = (0, 0, 255)
    pixels[3] = (255, 255, 0)
    pixels[4] = (0, 255, 255)
    pixels[5] = (255, 0, 255)
    pixels[6] = (255, 255, 255)
    pixels[7] = (63, 63, 63)
    pixels.show()
    time.sleep(1)

    pixels.fill((0, 0, 0))
    pixels.show()

    GPIO.cleanup()


if __name__ == "__main__":
    print("\nProgram started")
    if os.getuid() == 0:
        test()
    else:
        print("\nWS2812 test ommited - root/sudo privileges demanded.")
    print("\nProgram finished")
