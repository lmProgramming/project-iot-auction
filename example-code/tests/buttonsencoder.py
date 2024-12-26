#!/usr/bin/env python3

# pylint: disable=no-member

from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time

def ledsEnable():
    GPIO.output(led1, 1)
    GPIO.output(led2, 1)
    GPIO.output(led3, 1)
    GPIO.output(led4, 1)

def ledsDisable():
    GPIO.output(led1, 0)
    GPIO.output(led2, 0)
    GPIO.output(led3, 0)
    GPIO.output(led4, 0)

def ledsEnableForSecond():
    ledsEnable()
    time.sleep(1)
    ledsDisable()

def encoderTest():
    print("\n  The encoder test.")
    print("    Turn the encoder.")

    encoderLeftPrevoiusState = GPIO.input(encoderLeft)
    encoderRightPrevoiusState = GPIO.input(encoderRight)

    encoderLeftCounter = 0
    encoderRightCounter = 0

    while (encoderLeftCounter < 5 or encoderRightCounter < 5):
        encoderLeftCurrentState = GPIO.input(encoderLeft)
        encoderRightCurrentState = GPIO.input(encoderRight)

        if(encoderLeftPrevoiusState == 1 and encoderLeftCurrentState == 0):
            encoderLeftCounter += 1
        if(encoderRightPrevoiusState == 1 and encoderRightCurrentState == 0):
            encoderRightCounter += 1

        GPIO.output(led1, not encoderLeftCurrentState)
        GPIO.output(led2, not encoderRightCurrentState)

        encoderLeftPrevoiusState = encoderLeftCurrentState
        encoderRightPrevoiusState = encoderRightCurrentState

    ledsEnableForSecond()

def buttonsTest():
    print("\n  The buttons test.")

    print("    Press the red button.")
    GPIO.output(led3, 1)
    while(GPIO.input(buttonRed) == 1):
        pass
    ledsEnableForSecond()

    print("    Press the green button.")
    GPIO.output(led4, 1)
    while(GPIO.input(buttonGreen) == 1):
        pass
    ledsEnableForSecond()
    
def test():
    print('\nThe encoder and buttons test.')
    encoderTest()
    buttonsTest()
    print('\nThe encoder and buttons test finished sucessfully.')


if __name__ == "__main__":
    test()
    GPIO.cleanup()
