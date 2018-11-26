#!/usr/bin/env python3
import sucks
import configparser
from sucks.cli import *
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

# Reading the config file. In my system /root/.config/sucks.conf
# this config file is created by running 'sucks login'. Please refer to sucks documentation.
config = read_config()

# Sucks init
api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'])
my_vac = api.devices()[0]
# Device ID for a future multi device version
did=str(my_vac['did'])
print("Device ID: "+did)
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'], monitor=True)
vacbot.connect_and_wait_until_ready()

# MQTT INIT
mqttclient = mqtt.Client("sucks-gateway")
mqttclient.connect("192.168.1.2", port=8884, keepalive=60,bind_address="")

## ECOVACS ---> MQTT
## Callback functions. Triggered when sucks receives a status change from Ecovacs.
# Callback function for battery events
def battery_report(level):
    level_str=str(level*100)
    mqttpublish(did,"battery_level",level_str)
    print("Battery level: "+level_str)
    vacuum_report()

# Callback function for status events
def status_report(status):
    mqttpublish(did,"status",status)
    print("Status: "+status)
    vacuum_report() 
    
# Callback function for lifespan (components) events
def lifespan_report(lifespan):
    tipo=lifespan['type']
    valor=str(100*lifespan['lifespan'])
    mqttpublish(did,"components/"+tipo,valor)
    print("Lifespan: "+json.dumps(lifespan))
    print("tipo: "+tipo)
    print("valor: "+valor)

# Callback function for error events
# THIS NEEDS A LOT OF WORK
def error_report(mierror):
    error_str=str(mierror)
    mqttpublish(did,"error",error_str)
    print("Error: "+error_str)

# Library generated summary status. Smart merge of clean and battery status
# I think that when returning it should override "stop" values. Will follow on that.
def vacuum_report():
    mqttpublish(did,"vacuum",vacbot.vacuum_status)
    mqttpublish(did,"clean_status",vacbot.clean_status)
    print("Vacuum status:"+vacbot.vacuum_status)
    print("Clean status:"+vacbot.clean_status)
    if vacbot.fan_speed is not None:
        mqttpublish(did,"fan_speed",vacbot.fan_speed)
        print("Fan Speed: "+vacbot.fan_speed)
    mqttpublish(did,"charge_status",vacbot.charge_status)
    print("Charge Status: "+vacbot.charge_status)

# Publish to MQTT. Root topic should be in a config file or at least defined at the top.
def mqttpublish(did,subtopic,message):
    topic="ecovacs/"+did+"/"+subtopic
    mqttclient.publish(topic, message)
    
# Subscribe to the all event emitters
vacbot.batteryEvents.subscribe(battery_report)
vacbot.statusEvents.subscribe(status_report)
vacbot.lifespanEvents.subscribe(lifespan_report)
vacbot.errorEvents.subscribe(error_report)

# For the first run, try to get & report all statuses
vacbot.request_all_statuses
battery_report(vacbot.battery_status)

# These first two only reports when cleaning, so I ask for initial values here.
# For some reason, filter reports at start, but I ask it anyways in case this behaviour changes.
vacbot.run(GetLifeSpan("main_brush"))
vacbot.run(GetLifeSpan("side_brush"))
vacbot.run(GetLifeSpan("filter"))

## MQTT ----> Ecovacs
# Subscribe to this ecovac topics, translate mqtt commands into sucks commands to robot
subscribe_topic="ecovacs/"+did+"/command"
print("Subscribe topic: "+subscribe_topic)
mqttclient.subscribe(subscribe_topic)

def on_message(client, userdata, message):
    comando=str(message.payload.decode("utf-8")).lstrip()
    print("message received=",comando)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    if comando == "clean":
        vacbot.run(Clean())
    elif comando == "charge":
        vacbot.run(Charge())
    elif comando == "playsound":
        vacbot.run(PlaySound())    
    else:
        print("Comando desconocido")
        
mqttclient.on_message=on_message
mqttclient.loop_start()
# I assume here that the mqtt connection will be ok forever. I should probably test it and reconnect if necessary.

#vacbot.disconnect(wait=True) # Unused. This program is intended to run permanently.
