# test accelerometer (LIS2HH12)
# www.st.com/resource/en/datasheet/lis2hh12.pdfanslations/en.DM00096789.pdf
# based on this example
# https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/pysense-examples.html#pysense-examples
#

# test Ambient light sensor LTR-329ALS-01
# http://optoelectronics.liteon.com/en-global/Home/index
#

# test sensor MPL3115A2: I2C Barometric Pressure/Altitude/Temperature Sensor
# use official library
# http://www.nxp.com/assets/documents/data/en/data-sheets/MPL3115A2.pdf
# https://docs.pycom.io/pycom_esp32/library/machine.I2C.html
#

# test Temperature and humidity sensor (Si7006-A20)
# https://www.silabs.com/documents/public/data-sheets/Si7006-A20.pdf
#

from LIS2HH12 import LIS2HH12       	# 3-Axis Accelerometer
from LTR329ALS01 import LTR329ALS01 	# Digital Ambient Light Sensor
from raw2lux import raw2Lux  			# ... additional library for the light sensor
from MPL3115A2 import MPL3115A2			# Barometric Pressure Sensor with Altimeter
from SI7006A20 import SI7006A20  		# Humidity and Temperature Sensor
from pysense import Pysense

import machine
import math
import micropython
import pycom
import time

py = Pysense()

acc = LIS2HH12(py)
ambientLight = LTR329ALS01(py) 
pressure = MPL3115A2(py)
tempHum = SI7006A20(py)

while True:
    print('----------------------------------')

    print('X, Y, Z:', acc.read())
    print('Roll:', acc.roll())
    print('Pitch:', acc.pitch())
    print('Yaw:', acc.yaw())
    time.sleep(1)

    data = ambientLight.lux()
    LuxValue = raw2Lux(data)
    print("Read Ambient Light registers: {}   Lux: {}".format(data, LuxValue))
    time.sleep(1)

    temperature = pressure.temp()
    altitude = pressure.alt()
    print("Temperature: {} Degrees  Altitude: {}".format(temperature, altitude))
    time.sleep(1)

    temperature = tempHum.temp()
    humidity = tempHum.humidity()
    print("Temperature: {} Degrees  Humidity: {}".format(temperature, humidity))
    time.sleep(1)
    