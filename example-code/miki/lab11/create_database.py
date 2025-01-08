#!/usr/bin/env python3

import sqlite3
import time
import os
from constants import DATABASE_NAME, TABLE_NAME


def create_database():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("Old database was removed.")
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f""" CREATE TABLE {TABLE_NAME} (
        log_time text,
        uid text,
        num text
    )""")
    connection.commit()
    connection.close()
    print("New database was created.")


if __name__ == "__main__":
    create_database()
