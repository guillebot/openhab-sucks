# openhab-sucks

My attempt at monitor and control Ecovacs Deebot vacuum cleaners from OpenHAB

At the core, the great [sucks library](https://github.com/wpietri/sucks) by [@wpietri](https://github.com/wpietri)

# Installation

1. Follow the instructions at https://github.com/wpietri/sucks, basically:

`pip install sucks`

2. Run ```sucks login```, in order to generate the necesary ```sucks.conf``` config file

3. PLEASE TEST that you can run sucks correctly. Play with ```sucks clean 1```, ```sucks stop```

Only continue if you are sure that sucks it's running fine. If not please go to the great sucks community and ask for help.

4. Install dependencies

```pip install paho-mqtt```

5. Only if (3) it's ok: Clone this repo and run openhab-sucks.py

It should remain running, for that, I recommend [Supervisor](http://supervisord.org/)

# Concept

I'm using sucks library to connect to the Ecovacs system and monitor for status and activity.

At start and whenever it changes, I publish the values to my mqtt broker [Eclipse Mosquitto](https://mosquitto.org/). I use [MQTT](http://mqtt.org/) for all my IoT/Sensors communications to [OpenHAB](https://www.openhab.org/) and strongly recommend everybody to do so. MQTT it's standard, easy to deploy, easy to monitor from any device, and gives you the possibility of isolate devices from the home automation controller with a simple standard layer of abstraction. 

You can use the provided [ecovacs.items](https://github.com/guillebot/openhab-sucks/blob/master/openhab/ecovacs.items) and [ecovacs.sitemap](https://github.com/guillebot/openhab-sucks/blob/master/openhab/ecovacs.sitemap) to show the status.

It's very basic by now and it doesn't provides control. (I'm controlling the robot by system calling sucks, see To Do bellow)

# To do - Next steps

- Add more info. Consumables, etc.
- Add control. Put the openhab-sucks.py suscribed to mqtt and receive commands from openhab.
- (mine) Apply some logic with presence and automate ecovacs run daily.
