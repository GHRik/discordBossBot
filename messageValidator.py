from datetime import datetime
from messageFormater import split_content
from globals import COMMAND_LENGTH


def is_valid_date(date):
    format_date = "%d.%m.%Y"

    try:
        datetime.strptime(date, format_date)
        return True
    except ValueError:
        return False


def is_valid_time(time):
    time_format = "%H:%M"
    try:
        datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


def is_later_than_today(date, time):
    today = datetime.today().date()
    today_hours = datetime.today().time()
    today_date = str(today.day)+"."+str(today.month)+"."+str(today.year)
    today_hours = str(today_hours.hour)+":"+str(today_hours.minute)
    today_date = today_date+" "+today_hours

    my_date = date+" "+time

    format_date = "%d.%m.%Y %H:%M"
    today = datetime.strptime(today_date, format_date)
    my_day = datetime.strptime(my_date, format_date)

    if today < my_day:
        return True
    else:
        return False


def is_validate(command):
    split_context = split_content(command, '\\s+')
    if len(split_context) == COMMAND_LENGTH:
        split_context = split_content(split_context[1], "-")
        if len(split_context) == COMMAND_LENGTH:
            if is_valid_date(split_context[0]):
                if is_valid_time(split_context[1]):
                    if is_later_than_today(split_context[0], split_context[1]):
                        return True
    return False
