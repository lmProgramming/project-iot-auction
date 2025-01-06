from config import *

# sudo pip3 install mfrc522
import RPI.GPIO as GPIO
from mfrc522 import MRFC522
import time
import signal
from datetime import datetime

TIMEOUT_SECONDS = 3
MIFAREReader = MRFC522()
readTimes: dict[str, datetime] = {}


def readRFID():
    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status != MIFAREReader.MI_OK:
        return
    (status, uid) = MIFAREReader.MFRC522_Anticoll()
    if status != MIFAREReader.MI_OK:
        return

    uidStr = "".join([str(x) for x in uid])

    now = datetime.now()

    if uidStr not in readTimes:
        readTimes[uidStr] = now
        return processCard(uidStr, now)

    if (datetime.now() - readTimes[uidStr]).seconds > TIMEOUT_SECONDS:
        processCard(uidStr, now)

    readTimes[uidStr] = now


def processCard(uid: str, now: datetime):
    print(f"Card read: {uid} at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzerPin, GPIO.LOW)

    for led in [led1, led2, led3, led4]:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.1)
    for led in [led1, led2, led3, led4]:
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        while True:
            readRFID()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        GPIO.cleanup()
