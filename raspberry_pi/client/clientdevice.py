# an abstract class which will allow to change the device type (raspberry / desktop)

from abc import ABC, abstractmethod
import json
from raspberry_pi.client.auction.auction import Auction
from raspberry_pi.connection_config import *


class ClientDevice(ABC):
    current_auction: Auction = None

    @abstractmethod
    def displayAuction(self, auction, status):
        raise NotImplementedError
    
    @abstractmethod
    def displayWinner(self, auction):
        raise NotImplementedError
        
    @abstractmethod    
    def displayNothing(self):
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
                self.displayNothing()
                return print("No new autions.")
            if event == "auction_finished":
                self.displayWinner(self.current_auction)
                self.current_auction = None
                self.signal_registration()
            auction: Auction = Auction.fromJson(data["auction"])
            if self.current_auction and auction.id == self.current_auction and auction.price == self.current_auction.price:
                return
            if event == "new_auction":
                self.signal_registration()
            self.current_auction = auction
            self.displayAuction()

    @abstractmethod
    def displayNotLoggedIn(self):
        raise NotImplementedError

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

    @abstractmethod
    def signal_registration(self):
        raise NotImplementedError

