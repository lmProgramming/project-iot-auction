#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os
from config import *
import rfid
import RPi.GPIO as GPIO
import time
import datetime

os.environ["DISPLAY"] = "0.0"

# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()

uid: int | None = None
num: int | None = None
date_of_last_reading: datetime.datetime | None = None


def call_rfid_reading(uid, num) -> None:
    client.publish("uid/num", uid + "." + num)


def connect_to_broker() -> None:
    client.connect(broker)

    client.publish("message", "Client connected")


def disconnect_from_broker() -> None:
    client.publish("message", "Client disconnected")

    client.disconnect()


def buzzer(state) -> None:
    GPIO.output(buzzerPin, not state)  # pylint: disable=no-member


def stop() -> None:
    GPIO.cleanup()  # pylint: disable=no-member
    os._exit(0)


def run_sender() -> None:
    global uid, num
    GPIO.add_event_detect(buttonRed, GPIO.FALLING,
                          callback=stop, bouncetime=200)
    connect_to_broker()

    while True:
        uid, num = rfid.rfid_read()
        call_rfid_reading(str(uid), str(num))
        buzzer(True)
        time.sleep(.5)
        buzzer(False)
        time.sleep(.5)


if __name__ == "__main__":
    run_sender()
