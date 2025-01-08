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


def on_message(client, userdata, msg) -> None:
    payload = msg.payload.decode('utf-8')
    topic = msg.topic

    if topic.startswith("auction/"):
        auction_id = topic.split('/')[1]
        try:
            auction: Auction = Auction.objects.get(
                id=auction_id, is_active=True)
            user: User = User.objects.get(card_id=payload)

            if user.wallet.balance >= auction.current_price + PRICE_CHANGE:
                auction.current_price += PRICE_CHANGE
                user.save()
                auction.save()
                print(f"New bid: {
                      auction.current_price} by {user.name}")
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
