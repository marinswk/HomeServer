from urllib import request
from urllib.parse import quote
from dateutil.parser import parse
import json


class Station:

	def __init__(self, station_id, name):
		self.id = station_id
		self.name = name


class Travel:

	def __init__(self, station_id, direction, time, date, delay, platform, line_id, line_name, transport_type):
		self.station_id = station_id
		self.direction = direction
		self.time = time
		self.date = date
		self.delay = delay
		self.platform = platform
		self.line_id = line_id
		self.line_name = line_name
		self.transport_type = transport_type


def __fetch_url(url):
	try:

		req = request.Request(url)
		with request.urlopen(req) as response:
			response = response.read()

		return response

	except Exception as ex:

		print(ex)


def get_station_id_by_name(station_name):
	try:
		url = "https://1.bvg.transport.rest/locations?addresses=false&query=" + quote(station_name)

		result = __fetch_url(url)

		if not result:
			return None

		stations = json.loads(result)
		first_station = stations.pop(0)

		return Station(first_station['id'], first_station['name'])

	except Exception as ex:

		print(ex)
		raise ex


def get_station_departures(station_id, time=None):
	try:
		travels = []
		url = 'https://1.bvg.transport.rest/stations/' + station_id + '/departures'

		if time:
			url += '?when=' + time

		result = __fetch_url(url)

		if not result:
			return None

		result = json.loads(result)

		for _ in result:
			date = parse(_['when']) if _['when'] else _['when']
			travels.append(
				Travel(
					station_id=station_id,
					direction=_['direction'],
					time='{0:%H:%M}'.format(date) if _['when'] else _['when'],
					date='{0:%H:%M %d-%m-%Y}'.format(date) if _['when'] else _['when'],
					delay=_['delay'],
					platform=_['platform'],
					line_id=_['line']['id'],
					line_name=_['line']['name'],
					transport_type=_['line']['product']
				)
			)

		return travels
	except Exception as ex:

		print(ex)
		raise ex
