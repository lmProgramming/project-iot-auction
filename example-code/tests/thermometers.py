#!/usr/bin/env python3

from config import *  # pylint: disable=unused-wildcard-import
import w1thermsensor
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280



def ds18b20():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    print(f'\nDS18B200 Temp : {temp} '+chr(176)+'C')


def bme280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    #bme280.mode = adafruit_bme280.MODE_NORMAL
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    print('\nBME280:')
    print(f'Temperature: {bme280.temperature:0.1f} '+chr(176)+'C')
    print(f'Humidity: {bme280.humidity:0.1f} %')
    print(f'Pressure: {bme280.pressure:0.1f} hPa')
    print(f'Altitude: {bme280.altitude:0.2f} meters')


def test():
    print('\nThermometers test.')
    ds18b20()
    bme280()


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member
