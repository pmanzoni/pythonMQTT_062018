# MQTT Lab 1

This lab aims to offer you an hands-on experience with MQTT. You will perform experiments that will allow you to learn how to "publish" data and "subscribe" to get data. 


# Block 0: the client

For the experiment you will use the  (https://www.google.com/chrome/) and the MQTT Lens extension (https://chrome.google.com/webstore/search/mqttlens)

Once installed both you'll get something like this:
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

Let's create a connection to one of these broker. 

Click on the `+` sign on the top left part of the MQTT Lens window and add insert the following information

![](https://i.imgur.com/XZsDyvF.png)

Click on "CREATE CONNECTION" and you are done!

![](https://i.imgur.com/fQwCVmk.png)



# Block 2: some basic exercise

To perfom the following exercise some of you have to act as a "publisher" and some of you as a "Subscriber"

.....

Let's start with a easy one. In one of the small terminals write:
```shell
mosquitto_sub -t i/LOVE/Python
```
the broker terminal should show something like:

![](https://i.imgur.com/5nMOywi.png)

the broker registered the subscription request of the new client. Now in the other small terminal, execute:
```shell
mosquitto_pub -t i/LOVE/Python -m "Very well."
```
in the broker terminal, after the new registration messages, you'll also see something like:

![](https://i.imgur.com/s7zROiH.png)

meaning that the broker received the published message and that it forwarded it to the subscribed client. In the terminal where `mosquitto_sub` is executing you'll see the actual message appear.

Try now: 
```shell
mosquitto_pub -t i/love/python -m "Not so well"
```
**What happened? Are topics case-sensitive?**

Another useful option of `mosquitto_pub` is `-l`. Execute the following command:
```shell
mosquitto_pub -t i/LOVE/Python -l
```
and start typing some line of text. It sends messages read from stdin, splitting separate lines into separate messages. Note that blank lines won't be sent. You basically obtained a MQTT based **"unidirectional chat"** channel... 

### ... about Keepalive
By the way, if you kept the broker running with the `-v` option until now in a separate window, you can see various lines like:
```
1524673958: Sending PINGRESP to mosqpub|3592-iMac-de-Pi
1524673985: Received PINGREQ from mosqsub|3587-iMac-de-Pi
```
this simply shows that the broker and the client are interchanging these special messages to know whether they are still alive.


### QoS (Quality of Service):
Adding the `-q` option, for example to the `mosquitto_pub` you'll see the extra message that are now interchanged with the broker. For example, doing:
```shell
mosquitto_pub -t i/LOVE/Python -q 2 -m testing
```

you'll get:

![](https://i.imgur.com/wLqMrev.png)

compare this sequence of messages with the one obtained with `-q 0` or with `-q 1`.

### Retained messages:
Normally if a publisher publishes a message to a topic, and *no one is subscribed* to that topic the message is simply discarded by the broker. If you want your broker to remember the last published message, you'll have to use the ```retain``` option. Only one message is retained per topic. The next message published on that topic replaces the retained message for that topic. 
> To set the retain message flag you have to add `-r` using the Mosquitto clients.

So try the following cases, but  **remember now to always execute, for each test, the subscriber after** the publisher:
1. Publish a message with the retain message flag not set, like we did before. What happens?
1. Publish a message with the retain message flag set (`-r`). What happens?
1. Publish several (different) messages with the retain message flag set before starting the subscriber. What happens?
2. Publish a message with the retain message flag **not** set again. What happens?

Finally, how do I remove or delete a retained message? You have to publish a blank message(`-m ""`) with the retain flag set to true which clears the retained message. Try it.

