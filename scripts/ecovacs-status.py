import sucks
import configparser
from sucks.cli import *

config = read_config()

api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'])
my_vac = api.devices()[0]
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'])
vacbot.connect_and_wait_until_ready()

vacbot.run(Clean())  # start cleaning
time.sleep(9)      # clean for 15 minutes
vacbot.run(Charge()) # return to the charger
