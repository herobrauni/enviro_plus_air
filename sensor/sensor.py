import sys
import time
import smbus
import os
import json

from enviroplushat import ENVIROPLUS
from http.server import HTTPServer, BaseHTTPRequestHandler


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

    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp

    def sample(self):
        return self.apply_offsets(self.sensor.get_readings(self.sensor))

    def apply_offsets(self, measurements):
        # Apply any offsets to the measurements before storing them in the database
        if os.environ.get('SENSOR_TEMP_OFFSET') != None:
            if os.environ.get('SENSOR_OFFSET_FACTOR') != 0:
                measurements[0]['fields']['temperature'] = measurements[0]['fields']['temperature'] / float(os.environ['SENSOR_OFFSET_FACTOR']) + \
                    float(os.environ['SENSOR_TEMP_OFFSET'])
            else:
                measurements[0]['fields']['temperature'] = measurements[0]['fields']['temperature'] + \
                    float(os.environ['SENSOR_TEMP_OFFSET'])

        if os.environ.get('SENSOR_HUM_OFFSET') != None:
            measurements[0]['fields']['humidity'] = measurements[0]['fields']['humidity'] + \
                float(os.environ['SENSOR_HUM_OFFSET'])

        if os.environ.get('SENSOR_ALTITUDE') != None:
            # if there's an altitude set (in meters), then apply a barometric pressure offset
            altitude = float(os.environ['SENSOR_ALTITUDE'])
            measurements[0]['fields']['pressure'] = measurements[0]['fields']['pressure'] * (
                1-((0.0065 * altitude) / (measurements[0]['fields']['temperature'] + (0.0065 * altitude) + 273.15))) ** -5.257

        return measurements


class sensorHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        measurements = sensor.sample()
        self.wfile.write(json.dumps(measurements[0]['fields']).encode('UTF-8'))

    def do_HEAD(self):
        self._set_headers()


# Start the server to answer requests for readings
sensor = sensor()

while True:
    server_address = ('', 80)
    httpd = HTTPServer(server_address, sensorHTTP)
    print('Sensor HTTP server running')
    httpd.serve_forever()
