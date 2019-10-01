
def get_readable_hour(unix_time):
    '''Convert unix time to HH:MM:SS AM/PM format'''

    if (unix_time < 0) or (unix_time > 86399):
        raise Exception('Invalid unix_time: ' + str(unix_time))

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
