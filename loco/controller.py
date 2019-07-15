'''
Controller module handles the behavior of the service. Regardless or access method (HTTP Api, command-line)
the logic for executing the request is handled here.  As a controller all types should be native Python
as the access method is responsible for translating from Python types to that appopriate to the access method (example: Json, Txt)
'''

import os
from loco.google_location_client import client as gmapsclient
from loco.here_location_client import client as hmapclient

#TODO: Guard against missing parameters
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
HERE_APP_ID = os.environ.get('HERE_APP_ID')
HERE_APP_CODE = os.environ.get('HERE_APP_CODE')

__clients__ = []

def _initClients():
    """Only clients that have the proper configuration will be added to the list of geocode clients used.
    
    Raises:
        Exception: In the case no clients can be configured
    """
    global __clients__
    if GOOGLE_API_KEY:
        gmapsclient.init(GOOGLE_API_KEY)
        __clients__.append(gmapsclient.getlatlong)
    else:
        print("Missing GOOGLE_API_KEY environment setting, will not use Google")

    if HERE_APP_CODE and HERE_APP_ID:
        hmapclient.init(HERE_APP_CODE,HERE_APP_ID)
        __clients__.append(hmapclient.getlatlong)
    else:
        print("Missing either HERE_APP_CODE or HERE_APP_ID environment setting, will not use HERE")

    if __clients__ == []:
        raise Exception("No geocode client could be configured. Check the settings used.")


def search(address):

    locations = []

    for client_getlatlong in __clients__:
        locations.extend(client_getlatlong(address))
    
    for loc in locations:
        print("{provider}: lat: {lat}, lon: {lon}".format(lat=loc["lat"],lon=loc["lon"],provider=loc["provider"]))
    
    return locations

_initClients() # the init call will guard against starting without a viable service
