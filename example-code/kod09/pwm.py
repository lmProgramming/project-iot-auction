#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

def pwmTest():
    diode1 = GPIO.PWM(led1, 50)

    dutyCycle = 0
    diode1.start(dutyCycle)
    while dutyCycle < 100:
        time.sleep(0.2)
        dutyCycle += 10
        diode1.ChangeDutyCycle(dutyCycle)
    time.sleep(0.2)
    
    diode1.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    print("\nProgram started")
    pwmTest()
    print("\nProgram finished")
