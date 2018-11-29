from datetime import datetime, timezone
from urllib import request


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
		converted_date_one = datetime.utcfromtimestamp(date_one).replace(tzinfo=timezone.utc).astimezone(
			tz=None)
		converted_date_two = datetime.utcfromtimestamp(date_two).replace(tzinfo=timezone.utc).astimezone(
			tz=None)
		if converted_date_one < datetime.now().astimezone(tz=None) < converted_date_two:
			return True
		else:
			return False

	except Exception as ex:

		print(ex)
		raise ex
