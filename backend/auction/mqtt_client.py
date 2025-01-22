import time
import paho.mqtt.client as mqtt
from .models import Auction, User, Wallet
from django.utils import timezone
import threading
import atexit
import json

# MQTT Settings
# "10.108.33.125"  # Replace with the actual IP address
BROKER_ADDRESS = "10.108.33.123"
TOPIC = "auction/#"
NEW_TOPIC = "auction/news"

client = None  # Global client variable
# Global variable to store the active auction
active_auction: Auction = None


def get_next_auction() -> Auction:
    """
    Get the next auction to be activated.
    """
    return (
        Auction.objects.filter(
            is_finished=False,
            start_time__lt=timezone.now(),
        )
        .order_by("start_time")
        .first()
    )


def notify_new_auction(auction: Auction):
    """
    Notify clients immediately when a new auction is created and starts.
    """
    global client
    if not client:
        print("MQTT client is not initialized.")
        return

    payload = auction.create_payload(event="new_auction")
    try:
        client.publish(NEW_TOPIC, json.dumps(payload))
        print(f"Notified clients about new auction: {auction}")
    except Exception as e:
        print(f"Failed to notify clients about new auction: {e}")


def notify_auction_update(auction: Auction):
    """
    Notify clients during the auction about any updates like price changes.
    """
    global client
    if not client:
        print("MQTT client is not initialized.")
        return

    payload = auction.create_payload(event="auction_update")

    try:
        client.publish(NEW_TOPIC, json.dumps(payload))
        print(f"Notified clients about auction update: {auction}")
    except Exception as e:
        print(f"Failed to notify clients about auction update: {e}")


def notify_no_auctions():
    global client
    if not client:
        print("MQTT client is not initialized.")
        return
    payload = {"event": "no_auctions", "message": "No active auctions"}
    try:
        client.publish(NEW_TOPIC, json.dumps(payload))
        print("Notified clients about no active auctions")
    except Exception as e:
        print(f"Failed to notify clients about no active auctions: {e}")


def notify_auction_finished(auction: Auction):
    """
    Notify clients that the auction has finished.
    """
    global client
    if not client:
        print("MQTT client is not initialized.")
        return

    payload = auction.create_payload(event="auction_finished")
    if not auction.last_bidder:
        winner = "No one"
    else:
        winner = auction.last_bidder.name
    payload["auction"]["winner"] = winner
    try:
        client.publish(NEW_TOPIC, json.dumps(payload))
        print(f"Notified clients that auction has finished: {auction}")
    except Exception as e:
        print(f"Failed to notify clients about finished auction: {e}")


def on_connect(client, userdata, flags, rc):
    """
    Callback for when the client connects to the broker.
    """
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}")


def on_publish(client, userdata, mid):
    """
    Callback for when a message is published.
    """
    print(f"Message published with mid {mid}")


def on_message(client, userdata, msg) -> None:
    """
    Callback for when a message is received from the subscribed topics.
    """
    try:
        message: dict = json.loads(msg.payload.decode())
        event = message.get("event")
        if event and event == "bid":
            global active_auction
            auction_id = message.get("auction_id")
            card_uuid = message.get("card_uuid")
            if not auction_id or not card_uuid:
                raise ValueError("Auction ID and Card UUID are required.")
            wallet = Wallet.objects.get(card_id=card_uuid)
            if not wallet:
                raise ValueError("User not found.")
            if active_auction is None:
                raise ValueError("No active auction.")
            active_auction.bid(card_uuid)
            notify_auction_update(active_auction)
    except json.JSONDecodeError as e:
        print(f"Failed to decode MQTT message: {e}")
    except ValueError as e:
        print(f"Error processing message: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")


def start_mqtt():
    """
    Initializes and starts the MQTT client.
    """
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
        thread_client = threading.Thread(target=notify_clients, daemon=True)
        thread_client.start()

    except Exception as e:
        print(f"Failed to start MQTT client: {e}")


def notify_clients():
    """
    Notify clients about auctions.
    """
    global active_auction
    while True:
        try:
            now = timezone.now()
            if active_auction:
                if active_auction.end_time < now:
                    active_auction.finish_auction()
                    notify_auction_finished(active_auction)
                    active_auction = None
                else:
                    notify_auction_update(active_auction)

            else:
                next_auction = get_next_auction()
                if next_auction:
                    active_auction = next_auction
                    active_auction.start_auction()
                    notify_new_auction(active_auction)
                else:
                    notify_no_auctions()

        except Exception as e:
            print(f"Error notifying clients: {e}")
        time.sleep(5)


def stop_mqtt():
    """
    Disconnects and stops the MQTT client.
    """
    global client
    if client:
        try:
            client.disconnect()
            client.loop_stop()
            print("MQTT Client stopped")
        except Exception as e:
            print(f"Error stopping MQTT client: {e}")


# Ensure MQTT stops on Django shutdown
atexit.register(stop_mqtt)
