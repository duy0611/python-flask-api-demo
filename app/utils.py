from app.errors import InvalidUnixTime


MIN_UNIX_TIME = 0
MAX_UNIX_TIME = 86399


def get_readable_hour(unix_time: int) -> str:
    '''Convert unix time to HH:MM:SS AM/PM format'''

    if (unix_time < MIN_UNIX_TIME) or (unix_time > MAX_UNIX_TIME):
        raise InvalidUnixTime('Invalid unix_time: ' + str(unix_time))

    hours = unix_time // 3600 % 24
    minutes = unix_time // 60 % 60
    seconds = unix_time % 60

    suffix = 'AM'
    if hours >= 12:
        suffix = 'PM'

    if hours > 12:
        hours = hours - 12

    result = str(hours)
    if seconds > 0:
        result += ':' + str(minutes) + ':' + str(seconds)
    elif minutes > 0:
        result += ':' + str(minutes)

    return result + ' ' + suffix
