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
