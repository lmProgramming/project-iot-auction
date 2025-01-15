import json
from client.auction.auction import Auction
from client.clientdevice import ClientDevice
import keyboard

from connection_config import *  # Install with `pip install keyboard`
from decorators import debounce


class Windows(ClientDevice):

    def displayAuction(self):
        print(f"Windows: {self.current_auction}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Windows: on_connect - {rc}")
        super().on_connect(client, userdata, flags, rc, properties)

    def on_message(self, client, userdata, message):
        super().on_message(client, userdata, message)

    def on_publish(self, client, userdata, mid, retain=False, properties=None):
        print(f"Windows: on_publish - {mid}")

    def displayNotLoggedIn(self):
        print("Windows: Not logged in")

    def read_card(self):
        event = keyboard.read_event()
        if key := event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key.isdigit():
                return (int(key), 1)
        return (None, 0)

    def clear(self):
        pass
