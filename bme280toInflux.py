#!/home/pi/Documents/coding/GIT/python-bme280/env/bin/python
import sys
import time, smbus2, bme280, json
sys.path.append('/home/pi/Documents/coding/GIT/modules')
from Flux.Flux import Writer
from PointWriter.PointWriter import PointWriter


'''
This script will continually collect data from a bme280 sensor
on a raspberry PI and send the data to an influxDB instance in the cloud
This is setup to send data at a rate of roughly once per minute
'''

#read constants from configuration file
with open('/home/pi/Documents/coding/GIT/python-bme280/.configuration/db_settings.local.json') as jsondata:
    config = json.load(jsondata)

#open up a writer connection
db_writer = Writer(config['token'], config['org'], config['url'], config['bucket'])

#open connection to the sensor on the board
port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

#initialize data dict
data = {
        'temperature': -1,
        'humidity': -1
}

#setup base point
base_point = PointWriter(config['roomId'],('deviceId', config['deviceId']))

while True:
        test = bme280.sample(bus, address, calibration_params)
        data['temperature'] = (test.temperature * 9/5) +32
        data['humidity'] = test.humidity
        #check if valid value, and if not, try again
        if (20 < data['temperature'] < 100) and (0 < data['humidity'] < 100):
                temp_point = base_point.add_fields(data, time.time_ns())
                db_writer.write_data(temp_point)
                time.sleep(60)
                