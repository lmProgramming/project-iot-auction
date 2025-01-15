#!/usr/bin/env python3

# pylint: disable=no-member
import time
from mfrc522 import MFRC522


class RFID_READER:
    def __init__(self):
        self.MIFAREReader = MFRC522()

    def rfid_read(self) -> tuple[int, int]:
        counter = 0
        (status, _) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)
                print(f"Card read UID: {uid} > {num}")
                counter += 1
                return uid, num
