import unittest
import json

from app import create_app


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_opening_hours_convert_api(self):
        response = self.client.post(
            '/api/v1/opening_hours/convert',
            content_type='application/json',
            data=json.dumps({"friday": [{"type": "open", "value": 64800}], "saturday": [{"type": "close", "value": 3600}, {"type": "open", "value": 32400}, {"type": "close", "value": 39600}, {"type": "open", "value": 57600}, {"type": "close", "value": 82800}]}))

        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertTrue('Monday: Closed' in response_text)
        self.assertTrue('Tuesday: Closed' in response_text)
        self.assertTrue('Wednesday: Closed' in response_text)
        self.assertTrue('Thursday: Closed' in response_text)
        self.assertTrue('Friday: 6 PM - 1 AM' in response_text)
        self.assertTrue('Saturday: 9 AM - 11 AM, 4 PM - 11 PM' in response_text)
        self.assertTrue('Sunday: Closed' in response_text)
