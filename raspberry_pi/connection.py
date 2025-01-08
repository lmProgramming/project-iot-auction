from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime
# from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from config import *
import rfid

# configs
BROKER = "localhost"  # to be changed for ip
PORT = 1883
TOPIC_SUBSCRIBE = "auction/news"
TOPIC_PUBLISH = "auction/"


disp = SSD1331.SSD1331()
disp.Init()
disp.clear()

rfid_reader = MFRC522()

current_auction = {"auction_id": 1, "current_price": 100}

SOUND_ON = False

# fonts for display
# font_large = ImageFont.truetype('./lib/oled/Font.ttf', 18)
# font_small = ImageFont.truetype('./lib/oled/Font.ttf', 13)


def display_on_oled(auction, status):
    disp.clear()
    # image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    # draw = ImageDraw.Draw(image)

    # draw.text((5, 5), f"ID: {auction['id']}", font=font_small, fill="WHITE")
    # draw.text((5, 20), f"Article: {auction['article']}", font=font_small, fill="WHITE")
    # draw.text((5, 35), f"Price: ${auction['current_price']}", font=font_small, fill="WHITE")
    # draw.text((5, 50), f"Status: {status}", font=font_small, fill="BLUE")

    # disp.ShowImage(image, 0, 0)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_SUBSCRIBE)
    else:
        print(f"Failed to connect, return code {rc}")


def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")


def on_message(client, userdata, msg):
    global current_auction
    print(msg.topic)
    if msg.topic == TOPIC_SUBSCRIBE:
        current_auction = json.loads(msg.payload.decode("utf-8"))
        print(f"Received auction data: ID: {current_auction['auction_id']}, "
              f"Article: {current_auction['article']}, "
              f"Price: {current_auction['current_price']}")
        display_on_oled(current_auction, "Waiting for bids...")


def register_card(card_uid):
    global current_auction

    if current_auction:
        signal_registration()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # data to send to the server - depends on the json
        payload = {
            "timestamp": timestamp,
            "auction_id": current_auction["auction_id"],
            "card_uid": card_uid
        }

        id = current_auction["auction_id"]
        topic = f"{TOPIC_PUBLISH}{id}"

        client.publish(topic, json.dumps(payload))
        print(f"Card {card_uid} registered at {
              timestamp} for auction {current_auction['auction_id']}.")
        display_on_oled(current_auction, f"Card {card_uid} registered!")


def signal_registration():
    buzzer(True)
    time.sleep(0.2)
    buzzer(False)


def buzzer(state) -> None:
    if not SOUND_ON:
        return
    GPIO.output(buzzerPin, not state)  # pylint: disable=no-member


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(BROKER, PORT, 60)

    client.loop_start()

    # main loop
    try:
        print("Waiting for auction data...")
        while True:
            # maybe add checking if the card is the same as the last
            card_uid, num = rfid.rfid_read()
            if card_uid:
                register_card(card_uid)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()
        disp.clear()
        disp.reset()
