'''
Documentation on Google's Map API: https://developers.google.com/maps/documentation/geocoding
'''

import sys
import urllib.parse
import urllib.request
import json
import decimal
from loguru import logger

import loco.clientExceptions as clientExceptions

__apitoken__ = None


def init(apitoken=""):
    global __apitoken__
    __apitoken__ = apitoken
    return True


def _getlocationFromResult(jsonResult):
    return {"provider": "Google",
            "address": jsonResult["formatted_address"],
            "lat": jsonResult["geometry"]["location"]["lat"],
            "lon": jsonResult["geometry"]["location"]["lng"]}


def getlatlong(address):
    global __apitoken__
    
    params = urllib.parse.urlencode({'address': address, 'types':'street_address'})
    uri = "https://maps.googleapis.com/maps/api/geocode/json?{params}&key={apikey}".format(
        params=params, apikey=__apitoken__)
    logger.debug("Calling  " + uri)
    try:
        with urllib.request.urlopen(uri) as response:
            res_body = response.read().decode("utf-8")
            jsonpayload = json.loads(res_body, parse_float=decimal.Decimal)

    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise clientExceptions.PermissionDenied()
    except Exception:
        raise

    # Custom response processing for Google responses
    status = jsonpayload["status"]
    if status in ["ZERO_RESULTS"]:
        return []
    if status in ["OVER_DAILY_LIMIT", "OVER_QUERY_LIMIT", "UNKNOWN_ERROR"]:
        raise clientExceptions.QuotaLimit("Temporary error: {}".format(jsonpayload["status"]))
    if status in ["REQUEST_DENIED"]:
        raise clientExceptions.PermissionDenied("Problem with google account: {}".format(
            jsonpayload["status"]))
    if status in ["INVALID_REQUEST"]:
        raise clientExceptions.InvalidRequest("Problem with query: {}".format(
            jsonpayload["status"]))

    locations = [_getlocationFromResult(result)
                 for result in jsonpayload["results"]]

    return locations
