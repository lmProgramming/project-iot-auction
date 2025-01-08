#!/usr/bin/env python3

import sqlite3
import time
from datetime import datetime
import paho.mqtt.client as mqtt


broker = "localhost"
topic = "rfid/usage"
client = mqtt.Client()


def create_database():
    connection = sqlite3.connect("workers.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers_log (
            log_time TEXT,
            card_uid TEXT,
            terminal_id TEXT
        )
    """)
    connection.commit()
    connection.close()

# przychodzace wiadomosci


def process_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8")).split(",")
    if len(payload) == 2:
        card_uid, timestamp = payload
        terminal_id = "T_Martyna_Darek"
        print(f"Otrzymano: Karta {card_uid}, Czas: {
              timestamp}, Terminal: {terminal_id}")

        connection = sqlite3.connect("workers.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO workers_log VALUES (?, ?, ?)",
                       (timestamp, card_uid, terminal_id))
        connection.commit()
        connection.close()
    else:
        print("Nieprawidłowy format wiadomosci.")


def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.subscribe(topic)
    client.loop_start()
    print("Polaczono z brokerem MQTT i rozpoczeto subskrypcje.")


def main():
    create_database()
    connect_to_broker()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram zostal zatrzymany")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
