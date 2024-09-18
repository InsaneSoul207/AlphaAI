import datetime


def date():
    try:
        date = datetime.datetime.now().strftime("%b %d %Y")
    except Exception as e:
        print(e)
        date = False
    return date


def time():
    try:
        time = datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        print(e)
        time = False
    return time