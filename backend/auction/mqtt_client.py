import paho.mqtt.client as mqtt
from .models import Auction, User, Wallet
from django.utils import timezone
import threading
import os
import atexit
import datetime
import json
from .decorators import check_card_registration

# MQTT Settings
BROKER_ADDRESS = "localhost"  # change to ip
TOPIC = "auction/#"
NEW_TOPIC = "auction/news"

client = None  # Global client variable

PRICE_CHANGE = 50


# def new_auction():
#     payload = {
#         "auction_id": 1,
#         "current_price": 100,
#         "article": "miki",
#     }
#     client.publish(NEW_TOPIC, json.dumps(payload))

#     print("\n\n\nNEW AUCTION\n\n\n")

#     start_timer(10, new_auction)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")

    payload = {
        "auction_id": 1,
        "price": 100,
        "article": "miki",
    }
    client.publish(NEW_TOPIC, json.dumps(payload))

    client.subscribe(TOPIC)


def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")


def on_message(client, userdata, msg) -> None:
    check_card_registration(print(f"Received message: {msg.payload.decode()}"))


def start_timer(timer_time, method):
    def wrapper():
        method()

    timer = threading.Timer(timer_time, wrapper)
    timer.start()


def start_mqtt():
    global client
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_publish = on_publish

        client.connect(BROKER_ADDRESS, 1883, 60)
        thread = threading.Thread(target=client.loop_forever, daemon=True)
        thread.start()
        print("MQTT Client started")
    except Exception as e:
        print("MQTT Error:", e)


def stop_mqtt():
    global client
    if client:
        client.disconnect()
        client.loop_stop()
        print("MQTT Client stopped")


# Ensure MQTT stops on Django shutdown
atexit.register(stop_mqtt)
