import unittest
import json

from app.api import _convert_opening_hours_json


class OpeningHoursApiTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert_opening_hours(self):
        with open("examples/input.json", "r") as read_file:
            json_data = json.load(read_file)
            result = _convert_opening_hours_json(json_data)
            self.assertEqual(
                result, 'Monday: Closed\nTuesday: 10 AM - 6 PM\nWednesday: Closed\nThursday: 10 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM')

    def test_convert_opening_hours_not_full(self):
        json_data = json.loads(
            '{"friday":[{"type":"open","value":64800}],"saturday":[{"type":"close","value":3600},{"type":"open","value":32400},{"type":"close","value":39600},{"type":"open","value":57600},{"type":"close","value":82800}]}')
        result = _convert_opening_hours_json(json_data)
        self.assertEqual(
            result, 'Monday: Closed\nTuesday: Closed\nWednesday: Closed\nThursday: Closed\nFriday: 6 PM - 1 AM\nSaturday: 9 AM - 11 AM, 4 PM - 11 PM\nSunday: Closed')
