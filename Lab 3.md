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

Sending data 

# Step 3
Collecting data using MQTT
