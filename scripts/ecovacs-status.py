#!/usr/bin/env python3
import sucks
import configparser
from sucks.cli import *
import paho.mqtt.publish as publish
import json

# Reading the config file. In my system /root/.config/sucks.conf
# this config file is created by running 'sucks login'. Please refer to sucks documentation.
config = read_config()

api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'])
my_vac = api.devices()[0]
# Device ID for a future multi device version
did=str(my_vac['did'])
print("Device ID: "+did)
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'], monitor=True)
vacbot.connect_and_wait_until_ready()

## ECOVACS ---> MQTT

## Callback functions. Triggered when sucks receives a status change from Ecovacs.
# Callback function for battery events
def battery_report(level):
    level_str=str(level)
    mqttpublish(did,"battery",level_str)
    print("Battery: "+level_str)
    vacuum_report()

# Callback function for status events
def status_report(status):
    mqttpublish(did,"status",status)
    print("Status: "+status)
    vacuum_report() 
    
# Callback function for lifespan (components) events
# A esta funcion le falta bastante laburo porque lifespan puede ser muchas cosas. Puedo mandarlo en un solo json y pasarle el problema
# a openhab, o desarmar acá y reportar cada elemento en un topic distinto. Problema acá, facil en openhab.
def lifespan_report(lifespan):
    tipo=lifespan['type']
    valor=lifespan['lifespan']
    mqttpublish(did,"components/"+tipo,valor)
    print("Lifespan: "+json.dumps(lifespan))
    print("tipo: "+tipo)
    print("valor: "+valor)

# Callback function for error events
# This also needs some work in order to understand error object and send the correct mqtt message
def error_report(mierror):
    error_str=str(mierror)
    mqttpublish(did,"error",error_str)
    print("Error: "+error_str)

# Library generated summary status. Smart merge of clean and battery status
def vacuum_report():
    mqttpublish(did,"vacuum",vacbot.vacuum_status)
    print("Vacuum status:"+vacbot.vacuum_status)
    if vacbot.fan_speed is not None:
        mqttpublish(did,"fan_speed",vacbot.fan_speed)
        print("Fan Speed: "+vacbot.fan_speed)

# Publish to MQTT. Need to move harcoded values to config file or at least at the top of the file.
def mqttpublish(did,subtopic,message):
    topic="ecovacs/"+did+"/"+subtopic
    publish.single(topic, message, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")

# Subscribe to the all event emitters
vacbot.batteryEvents.subscribe(battery_report)
vacbot.statusEvents.subscribe(status_report)
vacbot.lifespanEvents.subscribe(lifespan_report)
vacbot.errorEvents.subscribe(error_report)

# For the first run, try to get & report all statuses
vacbot.request_all_statuses
vacbot.refresh_components
battery_report(vacbot.battery_status*100)
#charge_status=vacbot.charge_status
status_report(vacbot.clean_status)

## MQTT ----> Ecovacs
# Subscribe to this ecovac topics, translate mqtt commands into sucks commands to robot






#vacbot.disconnect(wait=True) # Unused. This program is intended to run permanently.

