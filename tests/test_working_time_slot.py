import unittest

from app.models import WorkingTimeSlot, DayOfWeek
from app.errors import InvalidWorkingTimeSlot


class WorkingTimeSlotTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model_valid(self):
        slot = WorkingTimeSlot(1, [], [])
        self.assertTrue(slot._isValid())

        slot = WorkingTimeSlot(2, [32400, 64800], [37800, 82800])
        self.assertTrue(slot._isValid())

    def test_model_not_valid(self):
        slot = WorkingTimeSlot(0, None, None)
        self.assertFalse(slot._isValid())

        slot = WorkingTimeSlot(2, [84800], [64800])
        self.assertFalse(slot._isValid())

        slot = WorkingTimeSlot(2, [36000], [64800, 84800])
        self.assertFalse(slot._isValid())

        slot = WorkingTimeSlot(2, [32400, 37800], [64800, 82800])
        self.assertFalse(slot._isValid())

    def test_get_readable_format(self):
        slot = WorkingTimeSlot(2, [32400, 64800], [37800, 82800])
        self.assertEqual(slot.getReadableFormat(), 'Tuesday: 9 AM - 10:30 AM, 6 PM - 11 PM')

    def test_get_readable_format_close_next_date(self):
        slot = WorkingTimeSlot(2, [32400, 64800], [37800, 89999])
        self.assertEqual(slot.getReadableFormat(), 'Tuesday: 9 AM - 10:30 AM, 6 PM - 1 AM')

    def test_get_readable_format_with_exception(self):
        slot = WorkingTimeSlot(2, [36000], [64800, 84800])
        with self.assertRaises(InvalidWorkingTimeSlot):
            slot.getReadableFormat()
