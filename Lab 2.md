# Lab 2

In this lab you will experiment about how MQTT can be used to send data to a cloud based platform. This procedure allows you to store your data in a cloud based repository and to analyze your data with software tools made available by the used platform.

For these experiments we will use the [Ubidots](https://ubidots.com/) plaftorm.
## Using Ubidots

You will have to first create your free account in the Ubidots platform here: https://app.ubidots.com/accounts/signup/ 

Then you have to add a **Device**:
![](https://i.imgur.com/ju1FfJo.png)


and then create a "Default" type variable:

![](https://i.imgur.com/sniIKoR.png)

You'll get something like this:
![](https://i.imgur.com/6PUeFKd.png)



Now we will send data to our device using MQTT. Take a look first to the Ubidots MQTT API Reference: https://ubidots.com/docs/api/mqtt.html

## First step: sending data using `MQTTlens`

We will first use `MQTTlens` to send data to the ``variable`` of our Ubidots  ``device``:

The name of the broker for educational users is "things.ubidots.com". To interact with it, you will need a TOKEN. The easiest way to get yours is clicking on “API Credentials” under your profile tab:

![](https://i.imgur.com/QMXvJL0.png)

In my case I have:

![](https://i.imgur.com/hKtcOng.png)

To connect to the MQTT broker you'll have to use your ``Default Token`` as the MQTT username, and put ``None`` in the password field.

![](https://i.imgur.com/pk0VpfK.png)


The **topic** you have to use is **`/v1.6/devices/{LABEL_DEVICE}/{LABEL_VARIABLE}`** where you have to replace the fields `{LABEL_DEVICE}` (e.g., kic-test-device) and `{LABEL_VARIABLE}`  (e.g., data-val).

> be careful that the `{LABEL_DEVICE}` and `{LABEL_VARIABLE}` are those indicated as ``API label``. For example: ![](https://i.imgur.com/p2HHVqa.png)


The data must be represented using JSON. The simplest format is: `{"value":10}` 

> the string ``value`` is fixed and defined by the Ubidots API


So, summing up, to send value 25 to variable `data-val` of device ``kic-test-device`` the topic must be:  

```
/v1.6/devices/kic-test-device/data-val
```

and the message:
```
{"value":25}
````
![](https://i.imgur.com/hsYr9Lj.png)


You'll get:
![](https://i.imgur.com/hjc8u6A.png)

So try to repeat all the previous steps with your own device and variable.


## Second step: sending data from a LoPy with the PySense board.

Using as a reference the information of the previous step, create a MicroPython periodic publisher that sends some values sensed with your  PySense to a specifically created variable in your Ubidots device.

Use as a reference the code examples in the directory https://github.com/pmanzoni/pythonMQTT_062018/tree/master/code

## Third step: creating dashbord elements.

Go to the Dashboard section and add new widget associated with the variable of your device.
![](https://i.imgur.com/YDQBZ4z.png)

See the alternatives you have and how they can be configured.


