from enum import Enum

from app import utils
from app.errors import InvalidWorkingTimeSlot


class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @staticmethod
    def from_str(label):
        if label.upper() == 'MONDAY':
            return DayOfWeek.MONDAY
        elif label.upper() == 'TUESDAY':
            return DayOfWeek.TUESDAY
        elif label.upper() == 'WEDNESDAY':
            return DayOfWeek.WEDNESDAY
        elif label.upper() == 'THURSDAY':
            return DayOfWeek.THURSDAY
        elif label.upper() == 'FRIDAY':
            return DayOfWeek.FRIDAY
        elif label.upper() == 'SATURDAY':
            return DayOfWeek.SATURDAY
        elif label.upper() == 'SUNDAY':
            return DayOfWeek.SUNDAY
        else:
            raise NotImplementedError


class WorkingTimeSlot:
    def __init__(self, day_of_week, opened_times, closed_times):
        self.day_of_week = day_of_week
        self.opened_times = opened_times if opened_times else []
        self.closed_times = closed_times if closed_times else []

    def appendTimeSlot(self, type, unixtime):
        if 'open' == type:
            self.opened_times.append(unixtime)
        elif 'close' == type:
            self.closed_times.append(unixtime)
        else:
            raise NotImplementedError

    def _isValid(self):
        # day of week between 1 and 7
        if self.day_of_week < 1 or self.day_of_week > 7:
            return False

        # open time and close time should be in pair
        if len(self.opened_times) != len(self.closed_times):
            return False

        # open time has to be smaller than close time
        if any([open_time >= close_time for open_time, close_time in zip(self.opened_times, self.closed_times)]):
            return False

        # next opened time has to be larger than previous closed time
        for i in range(len(self.opened_times) - 1):
            if self.opened_times[i+1] < self.closed_times[i]:
                return False

        return True

    def getReadableFormat(self):
        if not self._isValid():
            raise InvalidWorkingTimeSlot('Invalid working time slot: %s %s %s' % (
                self.day_of_week, self.opened_times, self.closed_times))

        str_result = ''
        str_result += DayOfWeek(self.day_of_week).name.capitalize() + ': '
        if len(self.opened_times) == 0:
            str_result += 'Closed'
        else:
            timeslots = [utils.get_readable_hour(open_time)
                         + ' - '
                         + utils.get_readable_hour(close_time if close_time <=
                                                   utils.MAX_UNIX_TIME else close_time - utils.MAX_UNIX_TIME)
                         for open_time, close_time in zip(self.opened_times, self.closed_times)]
            str_result += ', '.join(timeslots)

        return str_result
