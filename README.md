# openhab-sucks

My attempt at **monitor** and **control** [Ecovacs Deebot](https://www.ecovacs.com/us) vacuum cleaners from [OpenHAB](https://www.openhab.org/), via [MQTT](http://mqtt.org/).

At the core, the great [sucks library](https://github.com/wpietri/sucks) by [@wpietri](https://github.com/wpietri).

# Installation

1. Follow the instructions at https://github.com/wpietri/sucks, basically:

`pip install sucks`

2. Run ```sucks login```, in order to generate the necesary ```sucks.conf``` config file.

3. **PLEASE TEST** that you can run sucks correctly. Play with ```sucks clean 1```, ```sucks stop```. 

Only continue if you are sure that `sucks` it's running fine. If not please go to the great sucks community and ask for help.

4. Install dependencies

```pip install paho-mqtt```

5. If and only if (3) it's ok: Clone this repo and run `ecovacs-mqtt-gateway.py`

Run it with python3.

It should remain running in the background, for that, I recommend [Supervisor](http://supervisord.org/)

There is a provided supervisord [ecovacs.ini](https://github.com/guillebot/openhab-sucks/blob/master/supervisord/ecovacs.ini) example.

# Concept

I'm using sucks library to connect to the Ecovacs system and monitor for status and activity. At startup and whenever a status change is detected, it publishes the values to the mqtt broker [Eclipse Mosquitto](https://mosquitto.org/). It also listen for mqtt control messages to send commands to the vacuum cleaners.

I use [MQTT](http://mqtt.org/) for all my IoT/Sensors communications to [OpenHAB](https://www.openhab.org/) and strongly recommend everybody to do so. 

[MQTT](http://mqtt.org/) it's standard, lightewight, easy to deploy, easy to monitor from any device, and gives the possibility of isolate devices from the home automation controller with a simple standard layer of abstraction. 

If you are an OpenHAB user, you can use the provided [ecovacs.items](https://github.com/guillebot/openhab-sucks/blob/master/openhab/ecovacs.items) and [ecovacs.sitemap](https://github.com/guillebot/openhab-sucks/blob/master/openhab/ecovacs.sitemap) to show the status of your robots and/or control them.

If you are not an OpenHAB user, no matter how wrong you are, you can monitor and command via mqtt topics using your preferred software.

# Features

## Monitor

This gateway, when running, will listen from sucks events and update the following mqtt topics:

```
ecovacs/{did}/battery_level
ecovacs/{did}/battery_status
ecovacs/{did}/clean_status
ecovacs/{did}/vacuum
ecovacs/{did}/fan_speed
ecovacs/{did}/components/main_brush
ecovacs/{did}/components/side_brush
ecovacs/{did}/components/filter
```

#### Note:
`{did}` its the Device Id. It's something like E0000626317798704736. You can get it by running `ecovacs-mqtt-gateway.py` and it will show on the first line. Or you can also get it running `sucks --debug stop`, and it will be in a line like this:

`sucks      DEBUG    got {'todo': 'result', 'result': 'ok', 'devices': [{`**`'did': 'E0000693437743404736'`**`, 'name ...`

#### Example:

`ecovacs/E0345693817701104736/battery_level`

Keep in mind that this is simply a convention by me. This will be useful if in the future I decide to support more than one robot. If you understand this you can use anything you want in {did}, even something more human friendly like `/my_vacuum_cleaner/`

So from this on, you can use your usual mqtt consuming software to keep yourself posted of the Ecovacs whereabouts.

I use and recommend OpenHAB.

## Control

To control the vacuum cleaner via mqtt you have to publish `auto`, `charge`, `stop` or `playsound` message to the following topic:

`ecovacs/{did}/command`

#### Note:

I recommmend [MQTT.fx](https://mqttfx.jensd.de/) to monitor mqtt activity and do the troubleshooting.

# To do - Next steps

- Move some harcoded config (mqtt base topic, server, port) to some config file. 
- Error handling. Stuck here because sucks library it's giving me errors when I force errors. At least the most usual, like stuck robot. Is there a warning when it runs out of batteries returning?
- Test for stability on the mqtt connection. Reconnect if necessary.
- Test for stability in general. Monitor memory usage.
- (mine) Apply some logic with presence and automate ecovacs run daily.
- Adhere to Homie convention
- ~~Add control buttons on OpenHAB sitemap.~~ Done!

# Contact

Feel free to send push requests or drop me a line at: gschimmel at gmail dot com.

