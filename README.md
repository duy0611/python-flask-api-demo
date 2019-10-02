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

Pre-requisities: **Python3** and **Pip**

Install virtualenv with command: ```pip install virtualenv```

Create and activate the virtual enviroment:
```
cd python-flask-api-demo/

virtualenv venv
source venv/bin/activate
```

Install the missing python dependencies:
```
pip install -r requirements.txt
```

**Set FLASK_APP environment**
```
export FLASK_APP=flasky.py
export FLASK_ENV=development
```

**To run unit test**
```
flask test
```

**To run unit test with coverage**
```
flask test --coverage
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

In my opinion, I don't think this is the best way to store this kind of data as it is not that easy and straight-forward to serialize and deserialize the json data to certail class structure. Also, it's difficult to validate the json format with this structure unless we marshall the whole json to some object first and validate that object later. Last but not least, we have to remember special cases with this structure, like the case we had with the close time is on next date - this makes the marshalling logic more complex and easy to get some mistakes.

To make it better, I would go first with DB Schema (to store and retrieve these opening hours data) and the class structure of such:
```sql
CREATE TABLE OPENING_TIME_SLOTS (
    id bigint NOT NULL,
    restaurantId bigint NOT NULL,
    dayOfWeek int NOT NULL, --value is between 1 and 7
    openTime int NOT NULL, --e.g 3600
    closeTime int NOT NULL, --e.g. 64800
    PRIMARY KEY (ID)
)
```

The equivalent Entity class for this model is as following:
```python
class OpeningTimeSlot:
    # DAY_OF_WEEK
    # 1 = MONDAY
    # 2 = TUESDAY
    # 3 = WEDNESDAY
    # 4 = THURSDAY
    # 5 = FRIDAY
    # 6 = SATURDAY
    # 7 = SUNDAY
    def __init__(id, restaurant_id, day_of_week, open_time, close_time):
        self.id = id
        self.restaurant_id = restaurant_id
        self.day_of_week = day_of_week
        self.open_time = open_time
        self.close_time = close_time
```

By that, we will have the following json structure:
```json
[
    {
        "id": 1,
        "restaurant_id": 1,
        "day_of_week": 1,
        "open_time": 32400,
        "close_time": 39600
    },
    {
        "id": 2,
        "restaurant_id": 1,
        "day_of_week": 1,
        "open_time": 57600,
        "close_time": 82800
    },
    {
        "id": 3,
        "restaurant_id": 1,
        "day_of_week": 2,
        "open_time": 32400,
        "close_time": 90000 //1 AM next day
    }
    ....
]
```

Some of the advantages of this json/database structure:
- should be easier to serialize / descrialize the structure
- should be easier to filter and select only restaurants that opening now
- should be eaiser to add validation on class / json data structure
- don't have to care about specical cases: from the structure, we can clearly say that the retaurant can be opened/closed many times during the day of if it is closed on next day
- no need to deal with "Magic string": form the value we can say what day of week it is
- should be easier to add validation on open time / close time


