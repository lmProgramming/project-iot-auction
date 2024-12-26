#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

def blink():
    GPIO.output(led1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led1, GPIO.LOW)
    time.sleep(1)

def blinkTest():
    for i in range (5):
        blink()
    GPIO.cleanup()


if __name__ == "__main__":
    print("\nProgram started")
    blinkTest()
    print("\nProgram finished")
