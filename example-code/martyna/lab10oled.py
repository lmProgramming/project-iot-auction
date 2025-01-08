#!/usr/bin/env python3

from config import *  
import w1thermsensor
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import os
import math



def bme280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1020
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    # altitude = 44330 * (1.0 - math.pow(bme280.pressure / bme280.sea_level_pressure, 0.1903))
    altitude = 29.271 * (bme280.temperature + 273.15) * math.log(bme280.sea_level_pressure / bme280.pressure)
    print('\nBME280:')
    print(f'Temperature: {bme280.temperature:0.1f} '+chr(176)+'C')
    print(f'Humidity: {bme280.humidity:0.1f} %')
    print(f'Pressure: {bme280.pressure:0.1f} hPa')
    print(f'Altitude: {altitude:0.2f} meters')
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()
    rect = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(rect)
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    print("- draw text")
    draw.text((5, 15), f'H: {bme280.humidity:0.1f} %', font=fontSmall, fill="GREEN")
    draw.text((5, 0), f'T: {bme280.temperature:0.1f} '+chr(176)+'C', font=fontSmall, fill="GREEN")
    draw.text((5, 30), f'P: {bme280.pressure:0.1f} hPa', font=fontSmall, fill="GREEN")
    draw.text((5, 45), f'Alt: {altitude:0.2f} m', font=fontSmall, fill="GREEN")
    image = Image.open('./lib/oled/temp_s.jpg')
    image = image.resize((16, 16))
    rect.paste(image, (78, 0))
    image2 = Image.open('./lib/oled/hum_s.jpg')
    image2 = image2.resize((16, 16))
    rect.paste(image2, (78, 16))
    image3 = Image.open('./lib/oled/press_s.png')
    image3 = image3.resize((16, 16))
    rect.paste(image3, (78, 32))
    image4 = Image.open('./lib/oled/alt_s.png')
    image4 = image4.resize((16, 16))
    rect.paste(image4, (78, 48))
    disp.ShowImage(rect, 0, 0)
    time.sleep(5)
   





def test():
    print('\nThermometers test.')
    bme280()


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member