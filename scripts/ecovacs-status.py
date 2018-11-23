import sucks
import configparser
from sucks.cli import *

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
    time.sleep(10)

vacbot.disconnect(wait=True)
