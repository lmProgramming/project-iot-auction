#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

execute = True

def buttonPressedCallback(channel):
    global execute
    execute = False
    print("\nButton connected to GPIO " + str(channel) + " pressed.")

def redButtonTest():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)

    while execute:
        print('*', end='', flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    print("\nProgram started\n")
    redButtonTest()
    print("\nProgram finished")
