import time
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from config import *

disp = SSD1331.SSD1331()
disp.Init()
fontLarge = ImageFont.truetype("./lib/oled/Font.ttf", 20)
fontSmall = ImageFont.truetype("./lib/oled/Font.ttf", 13)


class bme280:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, 0x76)
        self.bme280.sea_level_pressure = 1013.25
        self.bme280.standby_period = adafruit_bme280.STANDBY_TC_500
        self.bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16

    def getTemperature(self):
        self.bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
        return self.bme280.temperature

    def getPressure(self):
        self.bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        return self.bme280.pressure

    def getHumidity(self):
        self.bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        return self.bme280.humidity

    def getHeight(self):
        return 44330 * (
            1 - (self.getPressure() / self.bme280.sea_level_pressure) ** (1 / 5.255)
        )


class Page:
    def __init__(self, picotgramPath, title, valueFunc):
        self.picogram = Image.open(picotgramPath).resize((24, 24))
        self.title = title
        self.valueFunc = valueFunc

    def show(self):
        disp.clear()
        image = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)
        value = round(self.valueFunc(), 2)

        draw.text((0, 0), self.title, font=fontLarge, fill="BLACK")

        image.paste(self.picogram, (0, 24))
        draw.text((26, 48), str(value), font=fontLarge, fill="BLACK")
        disp.ShowImage(image, 0, 0)


def handleButton(channel):
    global currentPage
    if channel == buttonRed:
        currentPage = (currentPage + 1) % len(pages)
        pages[currentPage].show()
    else:
        pages[currentPage].show()


GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=handleButton, bouncetime=350)
GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=handleButton, bouncetime=350)
currentPage = 0
bme = bme280()
temperature = Page("temperature.png", "Temperature", bme.getTemperature)
pressure = Page("pressure.png", "Pressure", bme.getPressure)
humidity = Page("humidity.png", "Humidity", bme.getHumidity)
height = Page("height.png", "Height", bme.getHeight)
pages = [temperature, pressure, humidity, height]
pages[currentPage].show()


while True:
    time.sleep(0.5)
