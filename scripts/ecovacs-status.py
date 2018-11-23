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

while True:
    print(vacbot.battery_status)
    print(vacbot.charge_status)
    print(vacbot.clean_status)
    publish.single("ecovacs/1/battery_status", vacbot.battery_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
    publish.single("ecovacs/1/charge_status", vacbot.charge_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
    publish.single("ecovacs/1/clean_status", vacbot.clean_status, hostname="192.168.1.2", port=8884, client_id="ecovacs-sucks")
    time.sleep(10)

vacbot.disconnect(wait=True)
