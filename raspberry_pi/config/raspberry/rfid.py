#!/usr/bin/env python3

# pylint: disable=no-member
import time
import RPi.GPIO as GPIO
from config.raspberry.raspberry_config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522


def rfid_read() -> tuple[int, int]:
    MIFAREReader = MFRC522()
    counter = 0
    while True:
        (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)
                print(f"Card read UID: {uid} > {num}")
                time.sleep(0.5)
                counter += 1
                return uid, num


def test():
    print("\nThe RFID reader test.")
    print("Place the card close to the reader (on the right side of the set).")
    rfid_read()
    print("The RFID reader tested successfully.")


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member
