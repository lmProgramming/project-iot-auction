#!/usr/bin/env python3
# pylint: disable=no-member

import RPi.GPIO as GPIO
from PIL import ImageFont

# pin numbers in BCM
SOUND_ON = False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 13
led2 = 12
led3 = 19
led4 = 26
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

buttonRed = 5
buttonGreen = 6
encoderLeft = 17
encoderRight = 27
GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

ws2812pin = 8

font_large = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18, layout_engine=ImageFont.LAYOUT_BASIC)
font_small = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 11, layout_engine=ImageFont.LAYOUT_BASIC)


def configInfo():
    print("This is only configuration file.\n")


if __name__ == "__main__":
    configInfo()
