from client.platform.windows import Windows
from connection_config import BROKER, PORT
import paho.mqtt.client as mqtt

device = Windows()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = device.on_message
client.on_connect = device.on_connect
client.on_publish = device.on_publish

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        card_uuid, num = device.read_card()
        if card_uuid:
            print(f"Card {card_uuid} registered.")
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    client.loop_stop()
    client.disconnect()
    device.clear()
