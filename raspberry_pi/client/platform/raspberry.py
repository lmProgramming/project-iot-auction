from client.clientdevice import ClientDevice
import config.raspberry.rfid as rfid
from config.raspberry.raspberry_config import *
from mfrc522 import MFRC522
from PIL import Image, ImageDraw, ImageFont
import config.raspberry.lib.oled.SSD1331 as SSD1331


class Raspberry(ClientDevice):
    def __init__(self):
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        self.disp.clear()
        self.rfid_reader = MFRC522()
        self.rfid = rfid.RFID()
        self.rfid.setup()

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
        return self.rfid.read_card()

    def clear(self):
        GPIO.cleanup()
        self.disp.clear()

    def display_auction(self, auction):
        self.disp.clear()
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text(
            (2, 10),
            f"Article: {
                auction['article']}",
            font=font_small,
            fill="WHITE",
        )
        draw.text(
            (2, 30),
            f"Price: ${
                auction['current_price']}",
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
