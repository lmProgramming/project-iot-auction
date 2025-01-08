#!/usr/bin/env python3

import time
from datetime import datetime
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from config import *

broker = "localhost"
topic = "rfid/usage"
client = mqtt.Client()

rfid_reader = MFRC522()

last_card_uid = None


def signal_registration():

    GPIO.output(buzzerPin, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzerPin, GPIO.HIGH)


def read_card():
    global last_card_uid
    (status, _) = rfid_reader.MFRC522_Request(rfid_reader.PICC_REQIDL)
    if status == rfid_reader.MI_OK:
        (status, uid) = rfid_reader.MFRC522_Anticoll()
        if status == rfid_reader.MI_OK:
            card_uid = sum(uid[i] << (i * 8) for i in range(len(uid)))
            if card_uid != last_card_uid:
                last_card_uid = card_uid
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Karta {card_uid} zarejestrowana o {timestamp}")

                client.publish(topic, f"{card_uid},{timestamp}")

                signal_registration()


def connect_to_broker():
    client.connect(broker)
    client.loop_start()
    print("Polaczono z brokerem MQTT.")


def main():
    connect_to_broker()
    print("Oczekiwanie na przyłożenie karty RFID...")
    try:
        while True:
            read_card()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram zostal zatrzymany")
    finally:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
