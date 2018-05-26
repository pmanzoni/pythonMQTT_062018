# MQTT Lab 2

This lab aims to offer you an hands-on experience with MQTT. You will perform experiments that will allow you to learn how to "publish" and "subscribe" to data. To this end you will use:
1. your own broker
1. a "sandbox" external broker
1. the **ThingSpeak** and **Ubidots** platform

You will learn how to:
* install and configure an MQTT broker
* interchange data using MQTT clients based on Python and MicroPython for the LoPy
* use MQTT to feed data to cloud based IoT platforms



# Block 4: Sending data to a cloud based platform

In this block you will experiment about how MQTT can be used to send data to a cloud based platform. This procedure allows you to store your data in a cloud based repository and to analyze your data with software tools made available by the used platform.

## Using ThingSpeak

ThingSpeak is an IoT analytics platform service that allows you to aggregate, visualize and analyze live data streams in the cloud. ThingSpeak provides instant visualizations of data posted by your devices to ThingSpeak. With the ability to execute MATLAB® code in ThingSpeak you can perform online analysis and processing of the data as it comes in. 

### Creating a *channel*
You first have to sign in. Go to https://thingspeak.com/users/sign_up and create your own account. Then you can create your first channel. Like for example:

![](https://i.imgur.com/siPq11m.png =300x400)


When a channel is created it is set as _private_. Set it to **public** as indicated in the figure below:

![](https://i.imgur.com/Dforjus.png)

Now you can take a look at it, as shown in the figure below. No data is plotted for the moment.

![](https://i.imgur.com/CYPVnr4.png)


You need the data in the API Keys section to connect to your channel. 

![](https://i.imgur.com/YZt82yB.png)


### Exercise
ThingSpeak offers either a REST and a MQTT API to work with channels. See here: https://es.mathworks.com/help/thingspeak/channels-and-charts-api.html

For this exercise you will need the documentation specific to **publish a message to update a single channel field** using MQTT. It is here: https://es.mathworks.com/help/thingspeak/publishtoachannelfieldfeed.html


#### First step: use `mosquitto_pub`

Use `mosquitto_pub` to send a value to your channel:

Consider that:
1. the hostname of the ThinSpeak MQTT service is "mqtt.thingspeak.com"
2. the topic you have to use is `channels/<channelID>/publish/fields/field<fieldnumber>/<apikey>` where you have to replace:
    * <channelID> with the channel ID,
    * <fieldnumber> with field number that you want to update, and 
    * <apikey> with the write API key of the channel. 
3. finally, remember that ThingSpeak requires you to:
    * set the PUBLISH messages to a QoS value of 0.
    * set the connection RETAIN flag to 0 (False).
    * set the connection CleanSession flag to 1 (True).
* Be careful!!!:
    * remember to add the string 'fields'
 channels/<channelID>/publish/**fields**/field<fieldnumber>/<apikey>
    * `field<fieldnumber>` means, for example, **field1**
    * use the **Write** API Key

#### Second step: use a Python program.

Using as a reference the code in file `paho-code/example4.py` in the GitHub repository, create a periodic publisher that sends the generated number to your ThingSpeak channel.

#### Third step: use a MicroPython program.

Using as a reference the code of the previous step, create a MicroPython periodic publisher that sends the generated number from your LoPy to your ThingSpeak channel.


## Using Ubidots

Repeat the previous exercise with the Ubidots platform. You will have to first create your free account here: https://app.ubidots.com/accounts/signup/ Then create a device:

![](https://i.imgur.com/CkHHqh3.png)

and then create a "Default" type variable:

![](https://i.imgur.com/ITZeABD.png)

Now we will send data to our device using MQTT. Take a look first to the MQTT API Reference: https://ubidots.com/docs/api/mqtt.html

#### First step: use `mosquitto_pub`

Use `mosquitto_pub` to send a value to your device:

Consider that:
1. the hostname for educational users is "things.ubidots.com". To interact with it, you will need a TOKEN. The easiest way to get yours is clicking on “API Credentials” under your profile tab:

![](https://i.imgur.com/QMXvJL0.png)

In my case I have:

![](https://i.imgur.com/72pXlm0.png)

To connect to the MQTT broker you'll have to use your Ubidots TOKEN as the MQTT username, and leave the password field empty.

2. the topic you have to use is **`/v1.6/devices/{LABEL_DEVICE}/{LABEL_VARIABLE}`** where you have to replace the fields `{LABEL_DEVICE}` (e.g., VLCtesting) and `{LABEL_VARIABLE}`  (e.g., my_value).

4. The data must be represented using JSON. The simplest format is: `{"value":10}` 

So, summing up, to send value 25 to variable `my_value` of device VLCtesting 

```
mosquitto_pub -h things.ubidots.com -u A1E-2DvBg......TsjaOcG4SRuTkgH -P '' 
              -t /v1.6/devices/vlctesting/my_value -m '{"value":25}'
```

> Be careful on the use of `'`and `"` and on the actual identifiers of the device and the variable (e.g., uppercase, lowercase, ...)
![](https://i.imgur.com/EEPGJaR.png =200x200)


You'll get:
![](https://i.imgur.com/xNFjzBv.png =400x300)

So try to repeat all the previous steps with your own device and variable.

#### Second step: use a Python program.

As before, and using as a reference the code in file `paho-code/example5-prod.py` in the GitHub repository, create a periodic publisher that sends the generated number to your Ubidots device.

#### Third step: use a MicroPython program.

Using as a reference the code of the previous step, create a MicroPython periodic publisher that sends the generated number from your LoPy to your Ubidots device.

