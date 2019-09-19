from datetime import datetime, timezone
from dateutil import tz
from urllib import request
from src.modules import db_operations


def fetch_url(url):
    try:

        req = request.Request(url)
        with request.urlopen(req) as response:
            response = response.read()

        return response

    except Exception as ex:

        print(ex)


def convert_utc_unix_timestamp_to_local_time_string(utc_string):
    try:
        return datetime.utcfromtimestamp(utc_string).replace(tzinfo=timezone.utc).astimezone(
            tz=None).strftime('%H:%M')
    except Exception as ex:

        print(ex)
        raise ex


def compare_dates(date_one, date_two):
    try:
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Berlin')
        converted_date_one = datetime.utcfromtimestamp(date_one).replace(tzinfo=from_zone).astimezone(to_zone)
        converted_date_two = datetime.utcfromtimestamp(date_two).replace(tzinfo=from_zone).astimezone(to_zone)

        if converted_date_one < datetime.now(to_zone) < converted_date_two:
            return True
        else:
            return False

    except Exception as ex:

        print(ex)
        raise ex


def get_config_dictionary():
    configurations = db_operations.read_configurations()
    config_dictionary = {x.name: x.value for x in configurations}
    return config_dictionary
