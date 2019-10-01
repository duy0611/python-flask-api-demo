# Opening Hours API

## Description

The REST API takes JSON-formatted opening hours of a restaurant
as an input and outputs hours in more human readable format.

Output example in 12-hour clock format:
```
Monday: 8 AM - 10 AM, 11 AM - 6 PM
Tuesday: Closed
Wednesday: 11 AM - 6 PM
Thursday: 11 AM - 6 PM
Friday: 11 AM - 9 PM
Saturday: 11 AM - 9 PM
Sunday: Closed
```

## How to run the program

Install virtualenv with command: ```pip install virtualenv```

Create and activate the virtual enviroment:
```
virtualenv venv
source venv/bin/activate
```

Install the missing python dependencies:
```
pip install -r requirements.txt
```

**To run unit test**
```
flask test
```

**To run the REST api**
```
flask run
```

The application will be available at: **http://localhost:5000/api/v1/**

The REST api is shipped with Swagger UI to help to debug and test the api. Example json input can be found from **examples/input.json** file

Example **curl** command:
```
curl -X POST "http://localhost:5000/api/v1/opening_hours/convert" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"thursday\": [ { \"type\": \"open\", \"value\": 64800 } ], \"friday\": [ { \"type\": \"close\", \"value\": 3600 } ], \"saturday\": [ { \"type\": \"open\", \"value\": 32400 }, { \"type\": \"close\", \"value\": 39600 }, { \"type\": \"open\", \"value\": 57600 }, { \"type\": \"close\", \"value\": 82800 } ]}"
```
## Thoughts about the current json data format


