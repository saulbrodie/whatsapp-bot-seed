from datetime import datetime, time


def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)


def get_countdown(year, month, day, hour='00', minutes='00'):
    target = '%s-%s-%s %s:%s:00' % (year, month, day, hour, minutes)
    leaving_date = datetime.strptime(target, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    return "%d days, %d hours, %d minutes, %d seconds" % daysHoursMinutesSecondsFromSeconds(
            dateDiffInSeconds(now, leaving_date))
