# an abstract class which will allow to change the device type (raspberry / desktop)

from abc import ABC, abstractmethod
import json
from client.auction.auction import Auction
from connection_config import *


class ClientDevice(ABC):
    current_auction: Auction = None

    @abstractmethod
    def displayAuction(self, auction, status):
        raise NotImplementedError

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(TOPIC_SUBSCRIBE)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, message):
        topic, payload = self.decode(message)
        if topic == TOPIC_SUBSCRIBE:
            data = json.loads(payload)
            event = data["event"]
            if event == EVENT_NOAUCTION:
                self.current_auction = None
                return print("No new autions.")
            auction: Auction = Auction.fromJson(data["auction"])
            self.current_auction = auction
            self.displayAuction()

    @abstractmethod
    def on_publish(self, client, userdata, mid):
        raise NotImplementedError

    @abstractmethod
    def read_card(self) -> tuple[int, int]:
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

    def decode(self, message) -> tuple[str, str]:
        return (message.topic, message.payload.decode("utf-8"))

    def __str__(self):
        return super().__str__()
