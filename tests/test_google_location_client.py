import json
import pathlib
import decimal

from loco.google_location_client import client

def test_parsing_normal_google_result(request):
    ''' This is a real test that is reprentative of the type of tests needed '''
    file = pathlib.Path(request.node.fspath)
    reffile = file.with_name('google_response.json')
    with reffile.open() as fp:
        response = json.load(fp,parse_float=decimal.Decimal)

    testResult = response["results"][0]  

    result = client._getlocationFromResult(testResult)
    reference = {"provider":"Google","lat":decimal.Decimal('38.90843479999999'),"lon":decimal.Decimal('-77.011087'),"address":"71 O St NW, Washington, DC 20001, USA"}
    print(result)

   # print([(a,b)for a,b in zip(result,reference)])
    assert result == reference