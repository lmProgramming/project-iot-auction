import paho.mqtt.client as mqtt
from .models import Auction, User, Wallet
from django.utils import timezone
import threading
import os
import atexit
import datetime
import json

# MQTT Settings
BROKER_ADDRESS = "10.108.33.129"
TOPIC = "auction/#"
NEW_TOPIC = "auction/news"

client = None  # Global client variable

PRICE_CHANGE = 50

def new_auction():
    payload = {
        "auction_id": 1,
        "current_price": 100,
        "article": "miki",
    }
    client.publish(NEW_TOPIC, json.dumps(payload))

    print("\n\n\nNEW AUCTION\n\n\n")

    start_timer(10, new_auction)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")

    payload = {
        "auction_id": 1,
        "price": 100,
        "article": "miki",
    }
    client.publish(NEW_TOPIC, json.dumps(payload))

    client.subscribe(TOPIC)

    start_timer(10, new_auction)

def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")


def on_message(client, userdata, msg) -> None:
    payload = msg.payload.decode('utf-8')
    topic = msg.topic

    if topic.startswith("auction/") and not topic.endswith("news"):
        print(topic)
        # todo: implement handling auction id
        auction_id = topic.split('/')[1]
        try:
            auction: Auction = Auction.objects.get(is_active=True)

            wallet: Wallet
            user: User
            wallets = Wallet.objects.filter(card_id=payload)
            if wallets:
                wallet = wallets[0]
                user = User.objects.get(wallet=wallet)
            else:
                wallet = Wallet.objects.create(
                    card_id=payload, balance=1000)

                user = User.objects.create(
                    name='John', surname='Doe', age=30, wallet=wallet)

            if user.wallet.balance >= auction.current_price + PRICE_CHANGE:
                auction.current_price += PRICE_CHANGE
                user.save()
                auction.save()
                print(f"New bid: {auction.current_price} by {user.name}")
            else:
                print("Insufficient funds")

            print(f"Payload: {payload}")

            current_auction = json.loads(payload)

            print(current_auction)

            payload = {
                "auction_id": auction_id,
                "price": auction.current_price + PRICE_CHANGE,
                "article": current_auction["article"],
            }
            client.publish("auction/1", json.dumps(payload))   
            
        except (Auction.DoesNotExist, User.DoesNotExist, Wallet.DoesNotExist) as e:
            print("Invalid auction or user:", e)
        except:
            print("error")


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
