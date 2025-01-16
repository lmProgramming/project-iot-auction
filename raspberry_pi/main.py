import json
import time
from raspberry_pi.connection_config import (
    BROKER,
    PORT,
    TOPIC_PUBLISH,
    TOPIC_SUBSCRIBE,
    check_logged_card,
)
import paho.mqtt.client as mqtt
import platform

if platform.system() == "Windows":
    from client.platform.windows import Windows

    device = Windows()
if platform.system() == "Linux":
    with open("/proc/cpuinfo", "r") as f:
        if "Raspberry Pi" in f.read():
            from raspberry_pi.client.platform.raspberry import Raspberry

            device = Raspberry()
        else:
            raise EnvironmentError(
                "Unsupported Linux platform. This script is designed for Raspberry Pi."
            )


client: mqtt.Client = mqtt.Client()
client.on_message = device.on_message
client.on_connect = device.on_connect
client.on_publish = device.on_publish

client.connect(BROKER, PORT, 60)
client.loop_start()

calls = {}


try:
    while True:
        try:
            card_uuid, num = device.read_card()
        except TypeError:
            continue

        if card_uuid:
            is_logged = check_logged_card(card_uuid)
            if not is_logged:
                device.displayNotLoggedIn()
                continue
            if not device.current_auction:
                continue
            payload = {
                "event": "bid",
                "card_uuid": card_uuid,
                "auction_id": device.current_auction.id,
            }
            rc, mid = client.publish(TOPIC_PUBLISH, payload=json.dumps(payload))
            time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    client.loop_stop()
    client.disconnect()
    device.clear()

import time
