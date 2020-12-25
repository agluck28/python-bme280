import time, board, busio, Adafruit_BME280, json
from Flux.Flux import Writer
from PointWriter.PointWriter import PointWriter


'''
This script will continually collect data from a bme280 sensor
on a raspberry PI and send the data to an influxDB instance in the cloud
This is setup to send data at a rate of roughly once per minute
'''

#read constants from configuration file
with open('.\\.configuration\\db_settings.json.local') as jsondata:
    config = json.load(jsondata)

#open up a writer connection
db_writer = Writer(config['token'], config['org'], config['bucket'], config['url'])

#open connection to the sensor on the board
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

#initialize data dict
data = {
        'temperature': -1,
        'humidity': -1
}

#setup base point
base_point = PointWriter('home',('room', 'Living_Room'))

while True:
        data['temperature'] = (bme280.temperature * 9/5) +32
        data['humidity'] = bme280.humidity
        #check if valid value, and if not, try again
        if (20 < data['temperature'] < 100) and (0 < data['humidity'] < 100):
                temp_point = base_point.add_fields(data, time.time_ns())
                time.sleep(60)