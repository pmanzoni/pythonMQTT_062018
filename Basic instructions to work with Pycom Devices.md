# Basic instructions to work with Pycom Devices

This document describes: 

1. the basic information required to set up a development environment, and 
2. the programming workflow for a Pycom device, in our case the LoPys. 

The main goal is to gain access to the REPL. REPL stands for Read Evaluate Print Loop, and is the name given to the interactive MicroPython prompt that is accessible on the Pycom Devices. Using the REPL is by far the easiest way to test out python code and run commands. 
More infos about REPL can be found here: https://docs.pycom.io/chapter/gettingstarted/programming/repl/

You must have Python3 installed in your computer. Check here https://www.python.org/download/releases/3.0/  for the proper instructions and code.

![](https://i.imgur.com/SGbpW1r.png)

## Installing mpy-repl-tool
mpy-repl-tool is the software tool that we will use to connect and control a LoPy (http://mpy-repl-tool.readthedocs.io/en/latest/index.html). 

To install it you have to execute: 
```
$ python3 -m pip install mpy-repl-tool
```

## Getting started with mpy-repl-tool

Plug-in your LoPy device in a USB port and wait a few seconds until the LED starts blinking in blue.

_NOTE: If you are using an OS inside a virtual machine, remember to tell the host machine to associate the device with your VM_


Then execute: 
```
$ python3 -m there detect
```
This command will list the serial ports and "hopefully" :smiley: will automatically find your LoPy board.

OK, now you are ready to start!

## Some usage examples

* to get a list of the files on the LoPy do: `$ python3 -m there ls -l /flash/*`
for example:
```
$ python3 -m there ls -l /flash/*
----------    0    0     34B 1980-01-01 01:09:16 /flash/main.py
----------    0    0     29B 1980-01-01 01:09:18 /flash/boot.py
```

> The filesystem has ``/`` as the root directory and the available physical drives are accessible from here. They are currently:
> ``/flash`` – the internal flash filesystem
> ``/sd`` – the SD card (if it exists)

* read the contents of a file on the LoPy:
```python3 -m there cat /flash/somefile```

* copy multiple files from your computer to the LoPy:
```python3 -m there push *.py /flash```

* backup all the files on the LoPy to your computer
```python3 -m there pull -r \* backup```

* finally, to start a serial terminal and get access to the [REPL](https://docs.pycom.io/chapter/toolsandfeatures/repl/) prompt add, exec:
```python3 -m there -i```

A detailed list of commands can be found here: http://mpy-repl-tool.readthedocs.io/en/latest/commandline.html

# Typical Lopy device workflow
A typical workflow is the following:

1. Create a folder on your computer
1. Plug your device into your USB port and exec:
```$ python3 -m there detect```
1. Write your code on your computer
1. Copy the code files from your computer to the LoPy
```$ python3 -m there push *.py /flash```
1. Start a serial terminal and get access to the REPL:
```$ python3 -m there -i```
1. Execute the code on the LoPy: e.g., `>>> import file` 

# Exercise: Let's see if it works

Execute the following code on your LoPy
```python=
import pycom
import time

RED = 0xFF0000
YELLOW = 0xFFFF33
GREEN = 0x007F00
OFF = 0x000000

def set_led_to(color=GREEN):
    pycom.heartbeat(False) # Disable the heartbeat LED
    pycom.rgbled(color)

def flash_led_to(color=GREEN, t1=1):
    set_led_to(color)
    time.sleep(t1)
    set_led_to(OFF)

flash_led_to(RED)
flash_led_to(YELLOW)
set_led_to(OFF)   
```

**Hint: save the code in a file named "test.py" for example and, in the REPL console, write ```import test```**

---
---

# How to

Below you'll find some generic information about how to connect and work with LoPys.

## Connect to a LoPy via WiFi

You can have access to the REPL also via a WiFi connection. Your LoPy by default works as a WiFi access point. Search an SSID that looks like `lopy-wlan-XXXX`; the password is  `www.pycom.io`:

![](https://i.imgur.com/dvGQbSI.png)

Then, you can access via telnet or via tools like Filezilla.

### Accesing via `telnet`:
Simply execute:
```telnet 192.168.4.1```and use as user/password the values *micro*/*python*.

### Accesing via Filezilla

If you want to interchange files with your LoPy you can use a tool like Filezilla:

1. Connect to device's WiFi (see above):

2. Go to top menu `File > Site Manager...` and use as the user/password pair the values *micro*/*python*:

![img/filezilla-settings.png](http://i.imgur.com/SAN02Pa.png)


## Resetting
They are different ways to reset your device. Pycom devices support both soft and hard resets. 

A **soft reset** clears the state of the MicroPython virtual machine but leaves hardware peripherals unaffected. To do a soft reset, 

* press Ctrl+D on the REPL or 
* execute:
```python
>>> import sys
>>> sys.exit()
```

A hard reset is the same as performing a power cycle to the device. In order to hard reset the device, press the reset switch or run:
```python
>>> import machine
>>> machine.reset()
```

If a device’s filesystem gets corrupted, it can format it by running:
```python
>>> import os
>>> os.mkfs('/flash')
```

then reboot.

More details here: https://docs.pycom.io/chapter/toolsandfeatures/bootmodes.html
