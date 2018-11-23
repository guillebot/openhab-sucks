import sucks
import configparser
from sucks.cli import *
import paho.mqtt.publish as publish


# Reading the config file. In my system /root/.config/sucks.conf
# this config file is created by running 'sucks login'. Refer to sucks documentation.
config = read_config()

api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'])
my_vac = api.devices()[0]
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'], monitor=True)
vacbot.connect_and_wait_until_ready()

# Ask values for the first time
battery_status=int(vacbot.battery_status*100)
charge_status=vacbot.charge_status
clean_status=vacbot.clean_status
# Publish values for the first time
publish.single("ecovacs/1/battery_status", battery_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
publish.single("ecovacs/1/charge_status", charge_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
publish.single("ecovacs/1/clean_status", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
print("Start battery status:", battery_status,'\n')
print("Start charge status:", charge_status,'\n')
print("Start clean status:", clean_status,'\n')

# Now loop forever and only send values when they change.
# I'm sure its a better version with callback functions when the library detects the changes
# but my python it's not enough
while True:
    if battery_status != int(vacbot.battery_status*100):
        battery_status=int(vacbot.battery_status*100)
        publish.single("ecovacs/1/battery_status", battery_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
        print("New battery status:", battery_status,'\n')
    if charge_status != vacbot.charge_status:    
        charge_status=vacbot.charge_status
        publish.single("ecovacs/1/charge_status", charge_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
        print("New charge status:", charge_status,'\n')
    if clean_status != vacbot.clean_status:
        clean_status = vacbot.clean_status   
        publish.single("ecovacs/1/clean_status", clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
        print("New clean status:", clean_status,'\n')
    time.sleep(5) # I don't know if each call to the vacbot object is putting strain on the network+xmpp or it is local

vacbot.disconnect(wait=True) # Unnecesary. I never exit this.

