from raspberry_pi.client.clientdevice import ClientDevice
from raspberry_pi.config.raspberry.rfid import RFID_READER
from raspberry_pi.config.raspberry.raspberry_config import *
from PIL import Image, ImageDraw, ImageFont
import raspberry_pi.config.raspberry.lib.oled.SSD1331 as SSD1331
import time
import base64
from io import BytesIO

class Raspberry(ClientDevice):
    last_message_received = None
    buzzerPin = 23
    SOUND_ON = True

    def __init__(self):
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        self.disp.clear()
        self.rfid = RFID_READER()

        #GPIO.setmode(GPIO.BCM) #idk if necessary should be already set
        GPIO.setup(buzzerPin, GPIO.OUT)
        GPIO.output(buzzerPin, 1)

    def buzzer(self, state: bool) -> None:
        if not self.SOUND_ON:
            return
        GPIO.output(self.buzzerPin, not state)  # pylint: disable=no-member

    def signal_registration(self):
        self.buzzer(True)
        time.sleep(0.2)
        self.buzzer(False)

    def display(self, auction, status):
        print(f"Raspberry: {auction} - {status}")

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print(f"Raspberry: on_connect - {rc}")

    def on_message(self, client, userdata, message):
        super().on_message(client, userdata, message)
        

    def on_publish(self, client, userdata, mid):
        print(f"Raspberry: on_publish - {mid}")

    def read_card(self):
        return self.rfid.rfid_read()

    def clear(self):
        GPIO.cleanup()
        self.disp.clear()

    def displayNotLoggedIn(self):
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), "Not logged in", font=font_large, fill="WHITE")
        self.disp.ShowImage(image, 0, 0)

    def displayNothing(self):
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        draw.text((2, 10),"Waiting for auction...",font=font_small,  fill="WHITE")

        self.disp.ShowImage(image, 0, 0)

    def displayWinner(self, auction):
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        draw.text((2, 10),f"{auction.last_bidder} won article: {self.current_auction.name}",font=font_small,  fill="WHITE")

        self.disp.ShowImage(image, 0, 0)

        time.sleep(5)


    def displayAuction(self):       
        print("I want to display auction")
        self.last_message_received = time.time()

        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text(           (2, 10),            f"Article: {                self.current_auction.name}",            font=font_small,  fill="WHITE",        )
        draw.text((2, 20), f"Price: ${self.current_auction.price}",font=font_small,fill="WHITE",)
        draw.text((2, 50), f"status", font=font_small, fill="BLUE")

        try:
            obj_array = self.current_auction.image
            binary_data = base64.b64decode(obj_array)
            artImg = Image.open(BytesIO(binary_data))

            #artImg = Image.open(
            #    '/home/pi/project-iot-auction/raspberry_pi/config/raspberry/lib/oled/pic.jpg'
            #)
            artImg = artImg.resize((30, 30))

            image.paste(artImg, (64, 36))
        except:
            print("error rendering image")

        self.disp.ShowImage(image, 0, 0)