#!/usr/bin/env python3
# coding=utf-8

import sys
import time
import scd30
import smbus
import os
import json

from enviroplushat import ENVIROPLUS
from http.server import HTTPServer, BaseHTTPRequestHandler

# scd30 init
PIGPIO_HOST = '::1'
I2C_SLAVE = 0x61
I2C_BUS = 1

sensor = scd30.SCD30(PIGPIO_HOST, I2C_SLAVE, I2C_BUS)
# trigger continous measurement
sensor.sendCommand(scd30.COMMAND_CONTINUOUS_MEASUREMENT, 970)

# enable autocalibration
sensor.sendCommand(scd30.COMMAND_AUTOMATIC_SELF_CALIBRATION, 1)
sensor.waitForDataReady()

# enviro init


class sensor():
    readfrom = 'unset'
    bus = smbus.SMBus(1)

    def __init__(self):
        # First, check for enviro plus hat (since it also has BME on 0x76)
        try:
            self.bus.write_byte(0x23, 0)  # test if we can connect to ADS1015
        except IOError:
            print('Enviro Plus hat not found')
        else:
            self.readfrom = 'enviroplus'
            self.sensor = ENVIROPLUS()
            print('Found Enviro+ Hat')

        # If this is still unset, no sensors were found; quit!
        if self.readfrom == 'unset':
            print('No suitable sensors found! Exiting.')
            sys.exit()

    def sample(self):
        return self.sensor.get_readings(self.sensor)


# Main Loop

try:
    while True:
        data = sensor.readMeasurement()

	if (data == False):
			exit(1)

		[float_co2, float_T, float_rH] = data

		if float_co2 > 0.0:
			print("gas_ppm{sensor=\"SCD30\",gas=\"CO2\"} %f" % float_co2)

		print("temperature_degC{sensor=\"SCD30\"} %f" % float_T)

		if float_rH > 0.0:
			print("humidity_rel_percent{sensor=\"SCD30\"} %f" % float_rH)


        measurements = sensor.sample()
        print(measurements)

		time.sleep(10)


except KeyboardInterrupt:
    sys.exit(0)
