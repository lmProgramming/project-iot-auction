from client.clientdevice import ClientDevice
from raspberry_pi.config.raspberry.rfid import RFID_READER
from config.raspberry.raspberry_config import *
from PIL import Image, ImageDraw, ImageFont
import config.raspberry.lib.oled.SSD1331 as SSD1331


class Raspberry(ClientDevice):
    def __init__(self):
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        self.disp.clear()
        self.rfid = RFID_READER()

    def display(self, auction, status):
        print(f"Raspberry: {auction} - {status}")

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print(f"Raspberry: on_connect - {rc}")

    def on_message(self, client, userdata, message):
        print(f"Raspberry: on_message - {message}")
        self.display_auction(message)

    def on_publish(self, client, userdata, mid):
        print(f"Raspberry: on_publish - {mid}")

    def read_card(self):
        return self.rfid.rfid_read()

    def clear(self):
        GPIO.cleanup()
        self.disp.clear()

    def displayNotLoggedIn(self):
        self.disp.clear()
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), "Not logged in", font=font_large, fill="WHITE")
        self.disp.ShowImage(image, 0, 0)

    def displayAuction(self):
        self.disp.clear()
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text(
            (2, 10),
            f"Article: {
                self.current_auction.name}",
            font=font_small,
            fill="WHITE",
        )
        draw.text(
            (2, 30),
            f"Price: ${
                self.current_auction.price}",
            font=font_small,
            fill="WHITE",
        )
        draw.text((2, 50), f"status", font=font_small, fill="BLUE")

        artImg = Image.open(
            "/home/pi/project-iot-auction/raspberry_pi/lib/oled/pic.jpg"
        )
        artImg = artImg.resize((30, 30))

        image.paste(artImg, (64, 10))
        self.disp.ShowImage(image, 0, 0)
