#!/usr/bin/env python3
import sucks
import configparser
from sucks.cli import *
import paho.mqtt.publish as publish
import json

# Reading the config file. In my system /root/.config/sucks.conf
# this config file is created by running 'sucks login'. Refer to sucks documentation.
config = read_config()

api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'])
my_vac = api.devices()[0]
did=my_vac['did']
print(did)
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'], monitor=True)
vacbot.connect_and_wait_until_ready()

# Callback function for battery events
def battery_report(level):
    print("inside battery_event callback")
    mqttpublish(my_vac,"battery",level)
    print(level)
    vacuum_report()

# Callback function for status events
def status_report(status):
    print("inside status_event callback")
    mqttpublish(my_vac,"status",status)
    print(status)
    vacuum_report() 
    
# Callback function for lifespan (components) events
# A esta funcion le falta bastante laburo porque lifespan puede ser muchas cosas. Puedo mandarlo en un solo json y pasarle el problema
# a openhab, o desarmar acá y reportar cada elemento en un topic distinto. Problema acá, facil en openhab.
def lifespan_report(lifespan):
    lifespan_str=json.dumps(lifespan)
    print("inside lifespan_event callback")
    mqttpublish(my_vac,"lifespan",lifespan_str)
    print(lifespan_str)

# Callback function for error events
def error_report(error):
    print("inside error_event callback")
    mqttpublish(my_vac,"error",error)
    print(error)

# Library generated summary status. Smart merge of clean and battery status
def vacuum_report():
    print("Inside vacuum_report")
    print(vacbot.vacuum_status)

# Publish to MQTT. Need to put harcoded values into config file or at least at the top of the file.
def mqttpublish(vac,subtopic,message):
    topic="ecovacs/"+vac+"/"+subtopic
    publish.single(topic, message, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")

# Subscribe to the all event emitters
vacbot.batteryEvents.subscribe(battery_report)
vacbot.statusEvents.subscribe(status_report)
vacbot.lifespanEvents.subscribe(lifespan_report)
vacbot.errorEvents.subscribe(error_report)

# For the first run, try to get & report all statuses
vacbot.request_all_statuses
vacbot.refresh_components

# When I first run, query all values and report them
# # Query values for the first time
battery_report(vacbot.battery_status*100)
#charge_status=vacbot.charge_status
status_report(vacbot.clean_status)
#vacuum_status=vacbot.vacuum_status
#fan_speed=vacbot.fan_speed
lifespan_report(vacbot.components)

# # Publish values for the first time
# publish.single("ecovacs/1/battery_status", battery_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# publish.single("ecovacs/1/charge_status", charge_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# publish.single("ecovacs/1/clean_status", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# publish.single("ecovacs/1/vacuum_status", vacuum_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# publish.single("ecovacs/1/fan_speed", fan_speed, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# publish.single("ecovacs/1/components", components, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
# # Debug info to console
# print("Start battery status:", battery_status)
# print("Start charge status:", charge_status)
# print("Start clean status:", clean_status)
# print("Start vacuum status:", vacuum_status)
# print("Start fan speed:", fan_speed)
# print("Start components:", components)

# # Now loop forever and only send values when they change.
# # I'm sure its a better version with callback functions when the library detects the changes
# # but my python it's not enough. This code sucks.
# while True:
#     if battery_status != int(vacbot.battery_status*100):
#         battery_status=int(vacbot.battery_status*100)
#         publish.single("ecovacs/1/battery_status", battery_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New battery status:", battery_status)
#     if charge_status != vacbot.charge_status:    
#         charge_status=vacbot.charge_status
#         publish.single("ecovacs/1/charge_status", charge_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New charge status:", charge_status)
#     if clean_status != vacbot.clean_status:
#         clean_status = vacbot.clean_status   
#         publish.single("ecovacs/1/clean_status", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New clean status:", clean_status)
#     if vacuum_status != vacbot.vacuum_status:
#         vacuum_status = vacbot.vacuum_status   
#         publish.single("ecovacs/1/vacuum_status", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New vacuum status:", vacuum_status)
#     if fan_speed != vacbot.fan_speed:
#         fan_speed = vacbot.fan_speed   
#         publish.single("ecovacs/1/fan_speed", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New fan speed:", fan_speed)
#     if components != json.dumps(vacbot.components):
#         components = json.dumps(vacbot.components)   
#         publish.single("ecovacs/1/components", components, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
#         print("New components:", components)
#     time.sleep(60) # I don't know if each call to the vacbot object is putting strain on the network+xmpp or it is local

#vacbot.disconnect(wait=True) # Unnecesary. I never exit this.

