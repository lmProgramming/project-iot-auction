from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

# configs
broker = "localhost"  # to be changed for ip
topic_current_auction = "auction/current"
topic_bid_submission = "auction/submission"

buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

disp = SSD1331.SSD1331()
disp.Init()
disp.clear()

rfid_reader = MFRC522()

current_auction = None

# fonts for display
font_large = ImageFont.truetype('./lib/oled/Font.ttf', 18)
font_small = ImageFont.truetype('./lib/oled/Font.ttf', 13)

def display_on_oled(auction_id, price, status):
    disp.clear()
    image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((5, 5), f"Auction ID: {auction_id}", font=font_small, fill="WHITE")
    draw.text((5, 25), f"Price: ${price}", font=font_large, fill="WHITE")

    draw.text((5, 50), status, font=font_small, fill="BLUE")

    disp.ShowImage(image, 0, 0)

# receiving auction data
def on_message(client, userdata, msg):
    global current_auction
    if msg.topic == topic_current_auction:
        current_auction = json.loads(msg.payload.decode("utf-8")) 
        print(f"Received auction data: ID: {current_auction['id']}, Price: {current_auction['price']}")
        display_on_oled(current_auction["id"], current_auction["price"], "Waiting for bids...")

# Function to register a card swipe
def register_card(card_uid):
    global current_auction

    if current_auction:
        signal_registration()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # data to send to the server - depends on the json
        payload = {
            "timestamp": timestamp,
            "auction_id": current_auction["id"],
            "card_uid": card_uid
        }
        client.publish(topic_bid_submission, json.dumps(payload))
        print(f"Card {card_uid} registered at {timestamp} for auction {current_auction['id']}.")
        display_on_oled(current_auction["id"], current_auction["price"], f"Card {card_uid} registered!")

def signal_registration():
    GPIO.output(buzzerPin, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzerPin, GPIO.HIGH)


def read_card():
    global last_card_uid
    (status, _) = rfid_reader.MFRC522_Request(rfid_reader.PICC_REQIDL)
    if status == rfid_reader.MI_OK:
        (status, uid) = rfid_reader.MFRC522_Anticoll()
        if status == rfid_reader.MI_OK:
            card_uid = sum(uid[i] << (i * 8) for i in range(len(uid)))
            return card_uid
    return None


# Connect to the MQTT broker
client = mqtt.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(topic_current_auction)
client.loop_start()

# Main loop to handle RFID reading
try:
    print("Waiting for auction data...")
    while True:
        card_uid = read_card()
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
