import sys
import os

from google_location_client import client as gmapsclient
from here_location_client import client as hmapclient

#TODO: Guard against missing parameters
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
HERE_APP_ID = os.environ.get('HERE_APP_ID')
HERE_APP_CODE = os.environ.get('HERE_APP_CODE')

def main():
    locations = []
    address = "80 Courter Ln"
    gmapsclient.init(GOOGLE_API_KEY)
    #locations.extend(gmapsclient.getlatlong(address))

    hmapclient.init(HERE_APP_CODE,HERE_APP_ID)
    locations.extend(hmapclient.getlatlong(address))
    
    for loc in locations:
        print("{provider}: lat: {lat}, lon: {lon}".format(lat=loc["lat"],lon=loc["lon"],provider=loc["provider"]))
    
    return True

if __name__ == "__main__":
    sys.exit(main())