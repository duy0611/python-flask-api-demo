import unittest
import json

from app.api import _convert_opening_hours_json


class OpeningHoursApiTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert_opening_hours_full(self):
        with open("examples/input.json", "r") as read_file:
            json_data = json.load(read_file)
            result = _convert_opening_hours_json(json_data)
            self.assertTrue('Monday: Closed' in result)
            self.assertTrue('Tuesday: 10 AM - 6 PM' in result)
            self.assertTrue('Wednesday: Closed' in result)
            self.assertTrue('Thursday: 10 AM - 6 PM' in result)
            self.assertTrue('Friday: 10 AM - 1 AM' in result)
            self.assertTrue('Saturday: 10 AM - 1 AM' in result)
            self.assertTrue('Sunday: 12 PM - 9 PM' in result)

    def test_convert_opening_hours_close_next_date(self):
        json_data = json.loads(
            '{"thursday":[{"type":"open","value":64800}],"friday":[{"type":"close","value":3600}],"saturday":[{"type":"open","value":32400},{"type":"close","value":39600},{"type":"open","value":57600},{"type":"close","value":82800}]}')
        result = _convert_opening_hours_json(json_data)
        self.assertTrue('Monday: Closed' in result)
        self.assertTrue('Tuesday: Closed' in result)
        self.assertTrue('Wednesday: Closed' in result)
        self.assertTrue('Thursday: 6 PM - 1 AM' in result)
        self.assertTrue('Friday: Closed' in result)
        self.assertTrue('Saturday: 9 AM - 11 AM, 4 PM - 11 PM' in result)
        self.assertTrue('Sunday: Closed' in result)
