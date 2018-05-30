# Lab 1

This lab aims to offer you an hands-on experience with MQTT. You will perform experiments that will allow you to learn how to "publish" data and "subscribe" to get data. 


# Block 0: the client

For the experiment you will use the Chrome browser (https://www.google.com/chrome/) and the MQTT Lens extension (https://chrome.google.com/webstore/search/mqttlens)

Once installed both, you'll get something like this:
![MQTT Lens splash](https://i.imgur.com/bgKxDlb.png)

# Block 1: Connecting to a public broker
> It is easy to install one's own broker. For example, one widely used is **Mosquitto**, which is part of the Eclipse Foundation and is an iot.eclipse.org project. Detailed installation indications can be found here: https://mosquitto.org/download/

In this session we will use a public broker. There are various public brokers in Internet, also called `sandboxes`. For example:
* `iot.eclipse.org`
    * more infos at: https://iot.eclipse.org/getting-started#sandboxes
* `test.mosquitto.org`
    * more infos at: http://test.mosquitto.org/
* `broker.hivemq.com`
    * more infos at: http://www.hivemq.com/try-out/
        * http://www.mqtt-dashboard.com/
        
we will always access them through port `1883`. 
Let's create a connection to one of these broker using MQTTlens. 

Click on the `+` sign on the top left part of the MQTT Lens window and insert the information indicated in the red rectangles. Then click on the ``Generate a random ID`` botton (actually you can insert whatever name you like in the ``Client ID`` field)

![](https://i.imgur.com/nTUf8gD.png)

Click now on the ``CREATE CONNECTION`` at the bottom of this window,  and if you get something like the image below, than you are connected to the ``iot.eclipse.org`` broker.

![](https://i.imgur.com/fQwCVmk.png)

As you can seen, in the Connection creation window there are various other fields that let you specify:
* the frequency of the Keep-alive timer (typically 60 seconds or 120 seconds)
* the username and password; we will use these fields in the next lab session
* the Last-will information

![](https://i.imgur.com/cFYtFTB.png)


# Block 2: some basic exercise

Let's start with a easy one. In the ``topic`` field of the Subscribe section write ``i/LOVE/Python`` and then click on the ``SUBSCRIBE`` button. The broker will register your subscription request.

![](https://i.imgur.com/xL8YB8e.png)

Now, in the ``topic`` field of the Pubish section write the same **identical** text for the topic (i.e., ``i/LOVE/Python``) and in the ``Message`` field write a text, whatever you want, like: ``Lecco is a beautiful city in Italy`` and click on the ``PUBLISH`` button.

You'll get something like the image below... **plus all the messages written by all the other clients in the room.** With just one publish action you actually reached various devices!!
![](https://i.imgur.com/MqORa3r.png)

> You can control the number of message that appear in the window using the + and - signs: ![](https://i.imgur.com/eaLtRBO.png)

### Are topics case-sensitive?

Write now in the ``topic`` field of the Pubish section the text: ``i/love/python``, that is all lowercase,  and in the ``Message`` field write a text, whatever you want, and click on the ``PUBLISH`` button.
**What happened? Did you receive any message?**


### Retained messages:
Normally if a publisher publishes a message to a topic, and *no one is subscribed* to that topic the message is simply discarded by the broker. If you want your broker to remember the last published message, you'll have to use the ``retained`` option.
Only one message is retained per topic. The next message published on that topic replaces the retained message for that topic. 
> With MQTTlens you have to click on the  ![](https://i.imgur.com/lJzRo1L.png) to set the retain message flag.

So try the following cases, but  **remember now to always subscribe,  in each case, after** the publisher:
1. Publish a message with the retain message flag not set, like we did before. What happens?
1. Publish a message with the retain message flag set. What happens?
1. Publish several (different) messages with the retain message flag set before subscribing. What happens?
2. Publish a message with the retain message flag **not** set again. What happens?

Finally, how do I remove or delete a retained message? You have to publish a blank message with the retain flag set to true. Try it.

# Block 3: a final exercise

Create groups of two or three devices. Now, using MQTTlens, create a very basic chat application, where all the messages published from any of the members  are received only by the members of the group