#!/usr/bin/env python3
# coding=utf-8

import time
import colorsys
import os
import sys
import scd30
import ST7735
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from enviroplus import gas
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json

# scd30 init
PIGPIO_HOST = '::1'
I2C_SLAVE = 0x61
I2C_BUS = 1

sensor_scd30 = scd30.SCD30(PIGPIO_HOST, I2C_SLAVE, I2C_BUS)
# trigger continous measurement
sensor_scd30.sendCommand(scd30.COMMAND_CONTINUOUS_MEASUREMENT, 970)

# enable autocalibration
sensor_scd30.sendCommand(scd30.COMMAND_AUTOMATIC_SELF_CALIBRATION, 1)
sensor_scd30.waitForDataReady()

# enviro init
# BME280 temperature/pressure/humidity sensor
bme280 = BME280()


# Main Loop
# sensor = sensor()

enviro_data = {}

try:
    while True:
        # get scd30 data
        data = sensor_scd30.readMeasurement()
        if (data == False):
            exit(1)

        [float_co2, float_T, float_rH] = data

        # get enviro data

        enviro_data["proximity"] = ltr559.get_proximity()
        enviro_data["raw_temp"] = bme280.get_temperature()
        enviro_data["pressure"] = bme280.get_pressure()
        enviro_data["humidity"] = bme280.get_humidity()
        enviro_data["light"] = ltr559.get_lux()
        enviro_gas = gas.read_all()
        enviro_data["ox"] = enviro_gas.oxidising / 1000
        enviro_data["red"] = enviro_gas.reducing / 1000
        enviro_data["nh3"] = enviro_gas.nh3 / 1000

        # Outputs
        print("temp: " + float_T + " co2: " + float_co2 + " hum: " + float_rH)
        print(enviro_data)
        time.sleep(10)


except KeyboardInterrupt:
    sys.exit(0)
