import time
import board
import busio
import adafruit_bme280
import socket
import json

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 15001
MULTICAST_TTL = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1011

while True:
        weather = {
            'temperature': bme280.temperature,
            'humidity': bme280.humidity,
            'pressure': bme280.pressure,
        }
        #print("\nTemperature: %0.1f C" % bme280.temperature)
        #print("Humidity: %0.1f %%" % bme280.humidity)
        #print("Pressure: %0.1f hPa" % bme280.pressure)
        #print("Altitude = %0.2f meters" % bme280.altitude)
        sock.sendto(json.dumps(weather).encode(), (MCAST_GRP, MCAST_PORT))
        time.sleep(2)
