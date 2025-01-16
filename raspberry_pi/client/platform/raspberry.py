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
        self.signal_registration()

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

    def displayNothing(self):
        disp = SSD1331.SSD1331()

        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()

        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text((2, 10),"Waiting for auction...",font=font_small,  fill="WHITE")

        self.disp.ShowImage(image, 0, 0)

    def displayWinner(self, auction):
        disp = SSD1331.SSD1331()

        # Initialize library.
        disp.Init()
        # Clear display.
        #disp.clear()

        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text((2, 10),f"{auction.last_bidder} won article: {self.current_auction.name}",font=font_small,  fill="WHITE")

        self.disp.ShowImage(image, 0, 0)

        time.sleep(5)


    def displayAuction(self):        
        #if self.last_message_received is not None and self.last_message_received < time.time() - 1:
        #    print(self.last_message_received)
        #    print(time.time())
        #    return
        print("I want to display auction")
        self.last_message_received = time.time()

        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLUE")
        draw = ImageDraw.Draw(image)

        # draw.text((5, 5), f"ID: {auction['auction_id']}", font=font_small, fill="WHITE")
        draw.text(           (2, 10),            f"Article: {                self.current_auction.name}",            font=font_small,  fill="WHITE",        )
        draw.text((2, 30), f"Price: ${self.current_auction.price}",font=font_small,fill="WHITE",)
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

        return

        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        fontLarge = ImageFont.truetype('/home/pi/project-iot-auction/raspberry_pi/config/raspberry/lib/oled/Font.ttf', 20)
        fontSmall = ImageFont.truetype('/home/pi/project-iot-auction/raspberry_pi/config/raspberry/lib/oled/Font.ttf', 13)

        print("- draw line")
        draw.line([(0, 0), (0, 63)], fill="BLUE", width=5)
        draw.line([(0, 0), (95, 0)], fill="BLUE", width=5)
        draw.line([(0, 63), (95, 63)], fill="BLUE", width=5)
        draw.line([(95, 0), (95, 63)], fill="BLUE", width=5)

        print("- draw rectangle")
        draw.rectangle([(5, 5), (90, 30)], fill="BLUE")

        print("- draw text")
        draw.text((8, 0), u'Hello', font=fontLarge, fill="WHITE")
        draw.text((12, 40), 'World !!!', font=fontSmall, fill="BLUE")

        # image1 = image1.rotate(45)
        disp.ShowImage(image1, 0, 0)
        time.sleep(2)

        print("- draw image")
        image = Image.open('/home/pi/project-iot-auction/raspberry_pi/config/raspberry/lib/oled/pic.jpg')
        disp.ShowImage(image, 0, 0)
        time.sleep(2)

        disp.clear()
        disp.reset()
        

        # self.disp.clear()
        
