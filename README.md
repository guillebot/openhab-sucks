# openhab-sucks

My attemp at monitor and control Ecovacs Deebot vacuum cleaners from OpenHAB

At the core, the great sucks library by @wpietri

https://github.com/wpietri

# Installation

1. Follow the instructions at https://github.com/wpietri/sucks, basically:

`pip install sucks`

2. Run ```sucks login```, in order to generate the necesary ```sucks.conf``` config file

3. TEST that you can run sucks correctly. Play with ```sucks clean 1```, ```sucks stop```

4. Install dependencies

```pip install paho-mqtt```

5. Only if (3) it's ok: Clone this repo and run openhab-sucks.py

It should remain running, for that, I recommend: http://supervisord.org/

# Concept

I'm using sucks library to connect to the Ecovacs system and monitor for status and status changes.

At start and whenever it changes, I publish the values to my mqtt broker (Eclipse Mosquitto https://mosquitto.org/). I use MQTT for all my IoT/Sensors communications to OpenHAB and strongly recommend everybody to do so. It's standard, easy to deploy, easy to monitor and I can play with a lot of other domotic solutions in case I ever get tired of OpenHAB (hope not, it's the best)

You can use the provided ecovacs.items and ecovac.sitemap to show the status.

It's very basic by now and it doesn't provides control.

# To do - Next steps

- Add more info. Consumables, etc.
- Add control. Put the openhab-sucks.py suscribed to mqtt and receive commands from openhab.
- (mine) Apply some logic with presence and automate ecovacs run daily.


