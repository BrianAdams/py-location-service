Geocoding Proxy Service
-----------------------

The Geocoding Proxy Service resolves the lattidue and longitude for a given address using third party geocoding serives. The Proxy Service will automatically try another geocoding service in the case the initial one fails.  This project is intended to be an example for building production Python services. 

When using the proxy, the service will return 1 or many results that include the lat,lng, as well as the full address that the service matched on.  In general, if the address you were expecting was not matched, you will need to provide a more complete address when querying.  

Swagger Documentation:
```
http://localhost:8000/docs
```



Example Query
```
curl -X GET "http://localhost:8000/geocoding?address=1313%20mockingbird%20lane" -H "accept: application/json"
```
Query response
```json
{
  "Results": [
    {
      "provider": "Here",
      "address": "Mockingbird Ln, Mississauga, ON L5N, Canada",
      "lat": 43.57321,
      "lon": -79.76483
    },
    {
      "provider": "Here",
      "address": "Mockingbird Ln, Beckwith, ON K0A, Canada",
      "lat": 45.11501,
      "lon": -76.06134
    }
  ]
}
```

```
docker build -t loco .
docker run -it -p <localport>:8000 --env-file=.env loco
```
Swagger Documentation:
```
http://localhost:<localport>/docs
```
```
gunicorn  loco.loco_fastapi.service:app -w 2 -k uvicorn.workers.UvicornWorker
```

```
uvicorn --workers 10 loco.loco_fastapi.service:app --no-access-log
```

```
env GOOGLE_API_KEY=<key> HERE_APP_ID=<key> HERE_APP_CODE=<key> -m loco query "1313 Mockingbird Lane" 
```

#### Options in the environment variables:

GOOGLE_API_KEY string, Developer key for Boogle API
HERE_APP_ID string, Developer app id for Here.com
HERE_APP_CODE string, Developer application code for Here.com
SERVER_PORT integer, Port that the service listens on, defaults to 8000

### Contributing

This is not an ongoing project. Feel free to clone and use this if you find it useful. I'm not planning on accepting an contributions or changes.