import json
from client.clientdevice import ClientDevice
import keyboard

from connection_config import TOPIC_SUBSCRIBE  # Install with `pip install keyboard`


class Windows(ClientDevice):
    def displayAuction(self, auction, status):
        print(f"Windows: {auction} - {status}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Windows: on_connect - {rc}")
        super().on_connect(client, userdata, flags, rc, properties)

    def on_message(self, client, userdata, message):
        topic, payload = self.decode(message)
        if topic == TOPIC_SUBSCRIBE:
            auction = json.loads(payload)
            print(
                f"Received auction data: ID: {auction['auction_id']}, "
                f"Article: {auction['article']}, "
                f"Price: {auction['current_price']}"
            )

    def on_publish(self, client, userdata, mid, retain=False, properties=None):
        print(f"Windows: on_publish - {mid}")

    def read_card(self):
        event = keyboard.read_event()
        if key := event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key.isdigit():
                return (int(key), 1)
        return (None, 0)

    def clear(self):
        pass
