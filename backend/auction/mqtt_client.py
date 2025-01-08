import paho.mqtt.client as mqtt
from .models import Auction, User
from django.utils import timezone
import threading
import os
import atexit

# MQTT Settings
BROKER_ADDRESS = "localhost"
TOPIC = "auction/#"

client = None  # Global client variable

PRICE_CHANGE = 50


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic

    if topic.startswith("auction/"):
        auction_id = topic.split('/')[1]
        try:
            auction = Auction.objects.get(id=auction_id, is_active=True)
            user = User.objects.get(card_id=payload)

            if user.balance >= auction.item.current_price + 1:
                auction.item.current_price += 1
                user.balance -= 1
                user.save()
                auction.item.save()
                print(f"New bid: {auction.item.current_price} by {user.name}")
            else:
                print("Insufficient funds")
        except (Auction.DoesNotExist, User.DoesNotExist) as e:
            print("Invalid auction or user:", e)


def start_mqtt():
    global client
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

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
