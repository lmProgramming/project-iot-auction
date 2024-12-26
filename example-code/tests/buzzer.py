#!/usr/bin/env python3

from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time

def buzzer(state):
    GPIO.output(buzzerPin, not state)  # pylint: disable=no-member

def test():
    print('\nBuzzer test.')
    buzzer(True)
    time.sleep(1)
    buzzer(False)


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member
