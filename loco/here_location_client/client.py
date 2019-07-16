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

def _getlocationFromResultParts(jsonResult):
    return {"provider": "Here",
            "address": jsonResult["Location"]["Address"]["Label"],
            "lat": jsonResult["Location"]["DisplayPosition"]["Latitude"],
            "lon": jsonResult["Location"]["DisplayPosition"]["Longitude"]}

def _getlocationFromResult(jsonResult):
  return [_getlocationFromResultParts(part) for part in jsonResult]

def getlatlong(address):
    global __appcode__
    global __appid___

    params = urllib.parse.urlencode({'searchtext':address,'app_code':__appcode__,'app_id':__appid___})
    uri = "https://geocoder.api.here.com/6.2/geocode.json?{params}".format(params=params)
    print(uri)

    try:
        with urllib.request.urlopen(uri) as response:
                res_body = response.read().decode("utf-8")
                jsonpayload = json.loads(res_body,parse_float=decimal.Decimal)
                if response.status != 200:
                  raise Exception("Unexpected Response")
                if jsonpayload["Response"]["View"] == []:
                  return [] #empty response
                  
                
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise Exception("Problem with Here account: {}".format(e.msg))
    except Exception:
            raise

    resultsections = [view["Result"] for view in jsonpayload["Response"]["View"]]

    locations = []
    for result in resultsections:
        locations.extend(_getlocationFromResult(result))

    return locations