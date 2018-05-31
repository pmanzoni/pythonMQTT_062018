import binascii
import machine
import micropython
import pycom
import socket
import struct
import sys
import time

from network import LoRa
from pysense import Pysense
from SI7006A20 import SI7006A20 		# Humidity and Temperature Sensor
from LTR329ALS01 import LTR329ALS01 	# Digital Ambient Light Sensor
from raw2lux import raw2Lux             # ... additional library for the light sensor


# SET HERE THE VALUES OF YOUR APP AND DEVICE
THE_APP_EUI = 'VOID'
THE_APP_KEY = 'VOID'


def join_lora(force_join = False):
    '''Joining The Things Network '''
    print('Joining TTN')

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        app_eui = binascii.unhexlify(THE_APP_EUI.replace(' ','')) # these settings can be found from TTN
        app_key = binascii.unhexlify(THE_APP_KEY.replace(' ','')) # these settings can be found from TTN

        # join a network using OTAA if not previously done
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not lora.has_joined():
            time.sleep(2.5)

        # saving the state
        lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            print('LoRa Joined')
            return True
        else:
            print('LoRa Not Joined')
            return False

    else:
        return True

# Let's see if you inserted the required data
if THE_APP_EUI == 'VOID':
	print("You must set the values of your app and device first!!")
	sys.exit()

# Getting the LoRa MAC
lora = LoRa(mode=LoRa.LORAWAN, public=1, adr=0, tx_retries=0)
print("Device LoRa MAC:", binascii.hexlify(lora.mac()))

# joining TTN
join_lora(True)

py = Pysense()
tempHum = SI7006A20(py)
ambientLight = LTR329ALS01(py) 

while True:
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
    s.setblocking(True)

    temperature = tempHum.temp()
    humidity = tempHum.humidity()
    luxval = raw2Lux(ambientLight.lux())

    print("Read sensors: temp. {} hum. {} lux: {}".format(temperature, humidity, luxval))

    # Packing sensor data as byte sequence using 'struct'
    # Data is represented as 3 float values, each of 4 bytes, byte orde 'big-endian'
    # for more infos: https://docs.python.org/3.6/library/struct.html
    payload = struct.pack(">fff", temperature, humidity, luxval)

    s.send(payload)

    time.sleep(15)
