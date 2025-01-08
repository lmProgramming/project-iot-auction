#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

execute = True


def buttonPressedCallback(channel):
    global execute
    execute = False
    print("\nButton connected to GPIO " + str(channel) + " pressed.")


def setup():
    print("\nProgram started\n")

    GPIO.add_event_detect(buttonRed, GPIO.FALLING,
                          callback=buttonPressedCallback, bouncetime=200)


def loop_step():
    print('*', end='', flush=True)
    time.sleep(0.1)


if __name__ == "__main__":
    setup()
    try:
        while True:
            loop_step()
    except KeyboardInterrupt:
        pass
    print("\nProgram finished")
