import paho.mqtt.client as mqtt
from .models import Auction, Article, User
from django.utils import timezone
import threading
import os

# MQTT Settings
BROKER_ADDRESS = "localhost"
TOPIC = "auction/#"


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
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(BROKER_ADDRESS, 1883, 60)
        thread = threading.Thread(target=client.loop_forever)
        thread.start()
    except Exception as e:
        print("MQTT Error:", e)
