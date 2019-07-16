'''
Documentation on Google's Map API: https://developers.google.com/maps/documentation/geocoding


The "status" field within the Geocoding response object contains the status of the request, and may contain debugging information to help you track down why geocoding is not working. The "status" field may contain the following values:

"OK" indicates that no errors occurred; the address was successfully parsed and at least one geocode was returned.
"ZERO_RESULTS" indicates that the geocode was successful but returned no results. This may occur if the geocoder was passed a non-existent address.
OVER_DAILY_LIMIT indicates any of the following:
The API key is missing or invalid.
Billing has not been enabled on your account.
A self-imposed usage cap has been exceeded.
The provided method of payment is no longer valid (for example, a credit card has expired).
See the Maps FAQ to learn how to fix this.

"OVER_QUERY_LIMIT" indicates that you are over your quota.
"REQUEST_DENIED" indicates that your request was denied.
"INVALID_REQUEST" generally indicates that the query (address, components or latlng) is missing.
"UNKNOWN_ERROR" indicates that the request could not be processed due to a server error. The request may succeed if you try again.
'''

import sys
import urllib.parse
import urllib.request
import json
import decimal

__apitoken__ = None

def init(apitoken=""):
    global __apitoken__
    print ('Google API key length:{size}'.format(size=len(apitoken)))
    __apitoken__ = apitoken
    return True

def _getlocationFromResult(jsonResult):
    return {"provider": "Google",
            "address": jsonResult["formatted_address"],
            "lat": jsonResult["geometry"]["location"]["lat"],
            "lon": jsonResult["geometry"]["location"]["lng"]}

def getlatlong(address):
    global __apitoken__
    params = urllib.parse.urlencode({'address':address})
    uri = "https://maps.googleapis.com/maps/api/geocode/json?{params}&key={apikey}".format(params=params,apikey=__apitoken__)
    print(uri)

    with urllib.request.urlopen(uri) as response:
        res_body = response.read().decode("utf-8")
        jsonpayload = json.loads(res_body,parse_float=decimal.Decimal)
        if response.status != 200:
            raise Exception("Unexpected Response")
        status = jsonpayload["status"]
        if status in ["ZERO_RESULTS"]:
                return []
        if status in ["OVER_DAILY_LIMIT","OVER_QUERY_LIMIT","UNKNOWN_ERROR"]:
                print("Temporary error: {}".format(jsonpayload["status"]))
                return []
        if status in ["REQUEST_DENIED"]:
                raise Exception("Problem with google account: {}".format(jsonpayload["status"]))
        if status in ["INVALID_REQUEST"]:
                raise Exception("Problem with query: {}".format(jsonpayload["status"]))       

    locations = [_getlocationFromResult(result) for result in jsonpayload["results"]]

    return locations