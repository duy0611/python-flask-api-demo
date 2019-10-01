import unittest

from app import utils
from app.errors import InvalidUnixTime


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_readable_hours_negative_time(self):
        with self.assertRaises(InvalidUnixTime):
            utils.get_readable_hour(unix_time=-1000)

    def test_get_readable_hours_over_max_time(self):
        with self.assertRaises(InvalidUnixTime):
            utils.get_readable_hour(unix_time=86400)

    def test_get_readable_hours(self):
        str_format = utils.get_readable_hour(unix_time=0)
        self.assertEqual(str_format, '0 AM')

        str_format = utils.get_readable_hour(unix_time=32400)
        self.assertEqual(str_format, '9 AM')

        str_format = utils.get_readable_hour(unix_time=37800)
        self.assertEqual(str_format, '10:30 AM')

        str_format = utils.get_readable_hour(unix_time=86399)
        self.assertEqual(str_format, '11:59:59 PM')
