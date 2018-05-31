# Lab 3

This Lab session will guide you through working with **The Things Networks** to send sensor data over LoRa to an application.


# Step 1
## Register with The Things Network

Manage your applications and devices via [The Things Network Console](https://console.thethingsnetwork.org/).

### Create an Account

To use the console, you need an account.
1.  [Create an account](https://account.thethingsnetwork.org/register).
2.  Select [Console](https://console.thethingsnetwork.org/) from the top menu.

### Add an Application in the Console

Add your first The Things Network Application.

![](https://i.imgur.com/8DLX3xZ.png)


1.  In the [Console](https://console.thethingsnetwork.org/), click [add application](https://console.thethingsnetwork.org/applications/add)

* For **Application ID**, choose a unique ID of lower case, alphanumeric characters and nonconsecutive `-` and `_` (e.g. `hi-world`).
* For **Description**, enter anything you like (e.g. `Hi, World!`).


![](https://i.imgur.com/olUsZ5p.png)


2.  Click **Add application** to finish.

    You will be redirected to the newly added application, where you can find the generated **Application EUI** and default **Access Key** which we'll need later.

![](https://i.imgur.com/JBfI9QK.png)


> If the Application ID is already taken, you will end up at the Applications overview with the following error. Simply go back and try another ID.
    
![](https://i.imgur.com/kL3Mozm.png)

### Register the Device

The Things Network supports the two LoRaWAN mechanisms to register devices: Over The Air Activation (OTAA) and Activation By Personalization (ABP). In this lab, we will use **OTAA**. This is more reliable because the activation will be confirmed and more secure because the session keys will be negotiated with every activation. ABP is useful for workshops because you don't have to wait for a downlink window to become available to confirm the activation.

1.  On the Application screen, scroll down to the **Devices** box and click **register device**.

![](https://i.imgur.com/hdmBYLm.png)


* As **Device ID**, choose a unique ID (for this application) of lower case, alphanumeric characters and nonconsecutive `-` and `_` (e.g., `my-device1`).
* As **Device EUI**, you have to use the value you get by executing in your LoPy the code in GitHub directory [code/getdevEUI.py](https://github.com/pmanzoni/pythonMQTT_062018/blob/master/code/getdevEUI.py)

![](https://i.imgur.com/HccYe7q.png)


2.  Click **Register**.

    You will be redirected to the newly registered device.
    
3.  On the device screen, select **Settings** from the top right menu.

![](https://i.imgur.com/RYaFXKs.png)

* You can give your device a description like `My first TTN device`
* Check that  *Activation method* is set to  *OTAA*.
* Uncheck **Frame counter checks** at the bottom of the page.

> **Note:** This allows you to restart your device for development purposes without the routing services keeping track of the frame counter. This does make your application vulnerable for replay attacks, e.g. sending messages with a frame counter equal or lower than the latest received. Please do not disable it in production.

4.  Click **Save** to finish.

    You will be redirected to the device, where you can find the **Device Address**, **Network Session Key** and **App Session Key** that we'll need next.
    
![](https://i.imgur.com/Ci9SGoC.png)


# Step 2

In this step we will use the device (the LoPy plus the PySense) registered in the step before to periodically send the sensed temperature, humidity and luminosity (lux). You will have to upload all the code in the directory [codcode/lab3_wpysense/](https://github.com/pmanzoni/pythonMQTT_062018/tree/master/code/lab3_wpysense)  **except** file `ttn_decode_thl.txt`.
**First**, clean the `/flash` memory of you device and  open for edit file `main.py`, and go to section:
```shell=python
...
# SET HERE THE VALUES OF YOUR APP AND DEVICE
THE_APP_EUI = 'VOID'
THE_APP_KEY = 'VOID'
...
``` 
and insert the proper values for your app and device. **Now, upload all the code to your LoPy.**

When you power up your device, file `main.py` should start executing automatically. If it doesn't send a Ctrl-D or push the soft-reset button. In the LoPy terminal you will see something like:
```
Device LoRa MAC: b'70b3d.....a6c64'
Joining TTN
LoRa Joined
Read sensors: temp. 30.14548 hum. 57.33438 lux: 64.64554
Read sensors: temp. 30.1562 hum. 57.31149 lux: 64.64554
...
```

Now, go in the Data section of your TTN application. You will see:
![](https://i.imgur.com/1D3xNEx.png)
The first line in the bottom is the message that represents the conection establishment and the other lines the incoming data.

If you click on any of the lines of the data, you'll get:

![](https://i.imgur.com/Dsaep1W.png)

where you can find a lot of information regarding the sending of you LoRa message.

If you check the Payload field, you will see a sequence of bytes... and that is actually what we sent :smile: 

To see what we actually sent, open once againg the file `main.py`, and go to section:

```shell=python=
...
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
    # Data is represented as 3 float values, each of 4 bytes, 
    #    byte orde 'big-endian'
    # for more infos: https://docs.python.org/3.6/library/struct.html
    payload = struct.pack(">fff", temperature, humidity, luxval)

    s.send(payload)

    time.sleep(15)
``` 

As you can see we are basically sending every 15 seconds the values of temperature, humidity and luminosity (lux) "compressed" as a sequence of 4*3= 12 bytes (:arrow_right: ``... = struct.pack(">fff",...``).

Now, to allow TTN to interpret these sequence of bytes we have to go the the section **Payload Format** and insert the code in file `ttn_decode_thl.txt` as is:

![](https://i.imgur.com/BsN17lI.png)

**IMPORTANT: remember to click on the "save payload function" button at the bottom of this window**

Go back to the Data window in TTN and start again you LoPy.

You will see that now even lines show some more infos:

![](https://i.imgur.com/q9vKiLX.png)

and if you click on any of the lines you will see:
![](https://i.imgur.com/HFR9jQa.png)

that is, the data in readable format.





# Step 3
TTN does not store the incoming data for a long time. If we want to keep these data, process  and visualize them, we need to use another platform... like for example Ubidots. In this step we will collect data from TTN and send it to Ubidots using MQTT.

We will first of all write the code necessary to access TTN through MQTT and read the incoming data. 

> All the details of the TTN MQTT API, can be found here: https://www.thethingsnetwork.org/docs/applications/mqtt/

Using [Google Colab](https://colab.research.google.com/) execute the code below. The code is also available in the [GitHub repository](https://github.com/pmanzoni/pythonMQTT_062018/tree/master/code/lab3_subpub), filename = 'subTTN'.

Remember to first properly set the vales for the username (`TTN_USERNAME`) which is the **Application ID** and the password (`TTN_PASSWORD`) which is the **Application Access Key**, in the bottom part of the _Overview_ section of the application window.
![](https://i.imgur.com/zUmWrqP.png)


```shell=python=
!pip install paho-mqtt

import sys
import time
import base64

import json
import struct

import paho.mqtt.client as mqtt

THE_BROKER = "eu.thethings.network"
THE_TOPIC = "+/devices/+/up"

# SET HERE THE VALUES OF YOUR APP AND DEVICE
TTN_USERNAME = "VOID"
TTN_PASSWORD = "VOID"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(THE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    themsg = json.loads(str(msg.payload))
    payload_raw = themsg["payload_raw"]
    payload_plain = base64.b64decode(payload_raw)
    print(payload_plain)

    vals = struct.unpack(">fff", payload_plain)

    print("Vals: temp. {} hum. {} lux: {}".format(vals[0], vals[1], vals[2]))



client = mqtt.Client()

# Let's see if you inserted the required data
if TTN_USERNAME == 'VOID':
    print("You must set the values of your app and device first!!")
    sys.exit()
client.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(THE_BROKER, 1883, 60)

client.loop_forever()
````

Now, with this code executing, **and your device generating data to TTN (as before)** you should start seeing data coming to your console:
![](https://i.imgur.com/ZzqUpFU.png)


What we have to do now is:
1. prepare Ubidots to receive our data
2. modify the previous code to upload it to Ubidots automatically

### phase 1: preparing Ubidots
Go to Ubidots, and following the steps of Lab. 2, create a device with the following variables:
![](https://i.imgur.com/3eWHvrn.png)

### phase 2: modify the code 

Using [Google Colab](https://colab.research.google.com/) execute the code below. The code is also available in the [GitHub repository](https://github.com/pmanzoni/pythonMQTT_062018/tree/master/code/lab3_subpub), filename = 'subTTN_pubUBI'.
Remember to first properly set the vales for `TTN_USERNAME`, `TTN_PASSWORD`, and `UBIDOTS_USERNAME`.


```shell=python=
import json
import sys
import time
import base64
import struct

import paho.mqtt.client as mqtt

TTN_BROKER = "eu.thethings.network"
TTN_TOPIC = "+/devices/+/up"

UBIDOTS_BROKER = "things.ubidots.com"

# SET HERE THE VALUES OF YOUR APP AND DEVICE
TTN_USERNAME = "VOID"
TTN_PASSWORD = "VOID"
UBIDOTS_USERNAME =  "VOID"


# The callback for when the client receives a CONNACK response from the server.
def on_connect_ttn(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TTN_TOPIC)

def on_connect_ubi(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

def on_message_ttn(client, userdata, msg):

    themsg = json.loads(str(msg.payload))
    payload_raw = themsg["payload_raw"]
    payload_plain = base64.b64decode(payload_raw)

    vals = struct.unpack(">fff", payload_plain)

    print("Vals: temp. {} hum. {} lux: {}".format(vals[0], vals[1], vals[2]))

    # JSONining the values according to the Ubidots API indications 
    payload = {"temperature": vals[0], "humidity": vals[1], "luxx": vals[2]}

    client_ubi.connect(UBIDOTS_BROKER, 1883, 60)
    client_ubi.loop_start()

    client_ubi.publish("/v1.6/devices/pysense1", json.dumps(payload))

    client_ubi.loop_stop()


client_ttn = mqtt.Client()
client_ubi = mqtt.Client()

# Let's see if you inserted the required data
if TTN_USERNAME == 'VOID':
    print("\nYou must set the values of your app and device first!!\n")
    sys.exit()
client_ttn.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)

# Let's see if you inserted the required data
if UBIDOTS_USERNAME == 'VOID':
    print("\nYou must set the values of Ubidots user first!!\n")
    sys.exit()
client_ubi.username_pw_set(UBIDOTS_USERNAME, password=None)

client_ttn.on_connect = on_connect_ttn
client_ubi.on_connect = on_connect_ubi
client_ttn.on_message = on_message_ttn

client_ttn.connect(TTN_BROKER, 1883, 60)

client_ttn.loop_forever()
````

As you can see, the code connects to the two brokers, reads from the TTN broker the incoming data, adapts the format of the data to the Ubidots API, and then publish it to the Ubidots broker.

Check in the Ubidots interface and you should see the incoming data. For example:

![](https://i.imgur.com/YdKRwQD.png)

