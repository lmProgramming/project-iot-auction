#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

def redButtonTest():
    while GPIO.input(buttonRed) == GPIO.HIGH :
        print('*', end='', flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    print("\nProgram started")
    redButtonTest()
    print("\nProgram finished")
