#!/home/pi/Documents/coding/GIT/python-bme280/env/bin/python
from RabbitHelper.RabbitHelper import Rabbit
import sys
import time
import smbus2
import bme280
import json
sys.path.append('/home/pi/Documents/coding/GIT/modules')


'''
This script will continually collect data from a bme280 sensor
on a raspberry PI and send the data to an influxDB instance in the cloud
This is setup to send data at a rate of roughly once per minute
'''

# read constants from configuration file
with open('/home/pi/Documents/coding/GIT/python-bme280/.configuration/db_settings.local.json') as jsondata:
    config = json.load(jsondata)

#setup routing key, needs to be a list
key = [f"bme280.{config['roomId']}.{config['deviceId']}"]

# open up a Rabbit connection
rabbit = Rabbit(config['url'], config['exchange'], key)

# open connection to the sensor on the board
port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# initialize data dict
data = {
    'time': time.time_ns(),
    'measurements': {
        'temperature': -1,
        'humidity': -1
    }
}


while True:
    test = bme280.sample(bus, address, calibration_params)
    data['measurements']['temperature'] = (test.temperature * 9/5) + 32
    data['measurements'] = test.humidity
    # check if valid value, and if not, try again
    if (20 < data['temperature'] < 100) and (0 < data['humidity'] < 100):
        data['time'] = time.time_ns()
        rabbit.send_message(data)
        time.sleep(60)
