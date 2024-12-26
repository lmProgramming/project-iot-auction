#!/usr/bin/env python3

# pylint: disable=no-member

from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time


def ledsDisable():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    GPIO.output(led4, False)


def simpleLedTest():
    ledsDisable()

    GPIO.output(led1, True)
    time.sleep(0.5)
    GPIO.output(led2, True)
    time.sleep(0.5)
    GPIO.output(led3, True)
    time.sleep(0.5)
    GPIO.output(led4, True)
    time.sleep(1)

    ledsDisable()


def pwmTest():
    diode1 = GPIO.PWM(led1, 50)  # New PWM instance
    diode2 = GPIO.PWM(led2, 50)  # New PWM instance
    dutyCycle = 1  # PWM duty cycle
    diode1.start(dutyCycle)  # PWM start
    diode2.start(dutyCycle)  # PWM start

    while dutyCycle <= 100:
        diode1.ChangeDutyCycle(dutyCycle)
        diode2.ChangeDutyCycle(dutyCycle)
        time.sleep(0.05)
        dutyCycle *= 1.1

    diode1.stop()
    diode2.stop()


def test():
    print('\nLED test.')
    simpleLedTest()
    pwmTest()


if __name__ == "__main__":
    test()
    GPIO.cleanup()
