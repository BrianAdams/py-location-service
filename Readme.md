Geocoding Proxy Service
-----------------------

This project is intended to be an example for building production Python services. It is current a work in progress!

The Geocoding Proxy Service resolves the latitude and longitude for a given address using third party geocoding services. The current service limits the geocode search to "street addresses", which is to say some APIs support seaching for points of interests, stores, etc... which is currently disabled.

Features:
* Automatic fallback to another geo-coding service on failure
* Integration with Google Maps and Here
* Command-line interface
  
When using the proxy, the service will return one or many results that include the lat,lng and the full address that the service matched on.  In general, if the address you were expecting was not matched, you will need to provide a more complete address when querying.  

### Getting Started:
The easiest way to experiment with the service is to spin it up in a docker container.
```
cp env.template .env
# replace api keys in the .env with your keys

docker build -t loco .

#this command will start docker on local port 8080. Change to something else if you have a conflict
docker run -it -p 8080:8000 --env-file=.env loco

```

You should see something similar to below when the service runs. You can press CTRL+C to kill it when done.
```shell
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO: Started parent process [6]
WARNING: email-validator not installed, email fields will be treated as str.
To install, run: pip install email-validator
WARNING: email-validator not installed, email fields will be treated as str.
To install, run: pip install email-validator
Google API key length:39
Google API key length:39
INFO: Started server process [7]
INFO: Waiting for application startup.
INFO: Started server process [8]
INFO: Waiting for application startup.
```

Now that the service is running you can try all of the following:

#### Browse API documentation
[Swagger](https://swagger.io/) is used to document the API:
```
http://localhost:8080/docs
```

You can use the Swagger documentation page to test out the API, or you can send queries using a tool like curl:
```shell
>curl -X GET "http://localhost:8000/v1/geocoding?address=1313%20mockingbird%20lane" -H "accept: application/json"
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
You will notice that the service will often return multiple results when the address that was sent was not precise enough to narrow the results to a single address.

### Running in productions
The docker container install uvicorn by default.  Below are the commands you can use to run the API service directly from the command-line where you can toggle many of the options you would use in a production environments:
```shell
#gunicorn (https://gunicorn.org/)
gunicorn  loco.loco_fastapi.service:app -w 2 -k uvicorn.workers.UvicornWorker

#uvicorn (uvicorn.org/)
uvicorn --workers 10 loco.loco_fastapi.service:app --no-access-log
```

### Command-line interface
The service has several options for running direct form the command-line
```shell
#Built in help
>./loco.py --help
Usage: loco.py [OPTIONS] COMMAND [ARGS]...

  This applciation will return the lat/lon from any one of several web
  services.

Options:
  --google_api_key TEXT
  --here_app_id TEXT
  --here_app_code TEXT
  --help                 Show this message and exit.

Commands:
  proxy  Start the API server
  query  Search for the given address

#Options can be passed in via environment variables or command-line options

>env GOOGLE_API_KEY=<key> HERE_APP_ID=<key> HERE_APP_CODE=<key> ./loco.py query "1313 Mockingbird Lane" 
```

#### Options in the environment variables:
```
GOOGLE_API_KEY string, Developer key for Google API
HERE_APP_ID string, Developer app id for Here.com
HERE_APP_CODE string, Developer application code for Here.com
SERVER_PORT integer, Port that the service listens on, defaults to 8000
```

### Contributing

This is not an ongoing project. Feel free to clone and use this if you find it useful. I'm not planning on accepting an contributions or changes.

#### Todo:
* Intergrate setup so that the application can simply be installed
* Expose configuration for enabling hooks for authentication
* Unit tests
* Find the error codes for HERE and unify them with an abstraction that works for all geocode services

#### Visual Studio Code integration
There are hooks for integrating with vscode using remote docker containers.  