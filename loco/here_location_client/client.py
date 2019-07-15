import sys
import urllib.parse
import urllib.request
import json
import decimal

__appcode__ = None
__appid___ = None

def init(appcode="",appid=""):
    global __appcode__
    global __appid___

    __appcode__ = appcode
    __appid___ = appid
    return True

def _getlocationFromResult(jsonResult):
    return {"provider": "Here",
            "address": jsonResult["Location"]["Address"]["Label"],
            "lat": jsonResult["Location"]["DisplayPosition"]["Latitude"],
            "lon": jsonResult["Location"]["DisplayPosition"]["Longitude"]}

def getlatlong(address):
    global __appcode__
    global __appid___

    params = urllib.parse.urlencode({'searchtext':address,'app_code':__appcode__,'app_id':__appid___})
    uri = "https://geocoder.api.here.com/6.2/geocode.json?{params}".format(params=params)
    print(uri)

    with urllib.request.urlopen(uri) as response:
        res_body = response.read().decode("utf-8")
        jsonpayload = json.loads(res_body,parse_float=decimal.Decimal)
        if response.status != 200:
            raise Exception("Unexpected Response")

    #TODO: Guard against non 1 line view sets
    locations = [_getlocationFromResult(result) for result in jsonpayload["Response"]["View"][0]["Result"]]

    return locations