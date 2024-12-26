#!/usr/bin/env python3

import time
import sqlite3
import tkinter
import paho.mqtt.client as mqtt
import os

os.environ["DISPLAY"] = "0.0"

'''Proszę przygotować zestaw dwóch programów wykorzystujących protokół MQTT do komunikacji między sobą.
Pierwszy to program obsługujący czytnik kart RFID. Program ten, jako wydawca (publisher) protokołu MQTT, będzie
wysyłał informację o identyfikatorze użytej karty i dokładnym czasie jej użycia. Proszę zadbać, aby karta RFID przyłożona
do czytnika była odczytywana jeden raz, jeśli jest stale przyłożona do czytnika. Proszę sygnałem dźwiękowym i wizualnym
poinformować użytkownika karty, że została ona odczytana.
Drugi program to klient, który jako subskrybent protokołu MQTT będzie odbierał informacje o użyciu kart RFID i zapisywał
fakt użycia.'''


# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

client = mqtt.Client()

window = tkinter.Tk()


def process_message(client, userdata, message) -> None:
    topic = message.topic
    # Decode message.
    message_decoded: list[str] = (
        str(message.payload.decode("utf-8"))).split(".")

    if topic == "uid/num":
        current_time: str = time.ctime()
        print(current_time + ", " +
              message_decoded[0] + " used the RFID card.")

        # Save to sqlite database.
        connention: sqlite3.Connection = sqlite3.connect("transactions.db")
        cursor: sqlite3.Cursor = connention.cursor()
        cursor.execute("INSERT INTO workers_log VALUES (?,?,?)",
                       (time.ctime(), message_decoded[0], message_decoded[1]))
        connention.commit()
        connention.close()
    else:
        print(" ; ".join(message_decoded))


def print_log_to_window() -> None:
    connention: sqlite3.Connection = sqlite3.connect("workers.db")
    cursor: sqlite3.Cursor = connention.cursor()
    cursor.execute("SELECT * FROM workers_log")
    log_entries = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entries:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
            "On %s, %s used the terminal %s" % (log_entry[0], log_entry[1], log_entry[2]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connention.commit()
    connention.close()

    print_log_window.mainloop()


def create_main_window():
    window.geometry("250x100")
    window.title("RECEIVER")
    label = tkinter.Label(window, text="Listening to the MQTT")
    exit_button = tkinter.Button(window, text="Stop", command=window.quit)
    print_log_button = tkinter.Button(
        window, text="Print log", command=print_log_to_window)

    label.pack()
    exit_button.pack(side="right")
    print_log_button.pack(side="right")


def connect_to_broker() -> None:
    client.connect(broker)

    client.on_message = process_message

    client.loop_start()
    client.subscribe("message")
    client.subscribe("uid/num")


def disconnect_from_broker() -> None:
    client.loop_stop()
    client.disconnect()


def run_receiver() -> None:
    connect_to_broker()
    create_main_window()

    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
