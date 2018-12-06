from flask import session
from urllib.parse import quote
from dateutil.parser import parse
from Support import fetch_url
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


def get_station_id_by_name(station_name):
	try:
		url = "https://1.bvg.transport.rest/locations?addresses=false&query=" + quote(station_name)

		response = fetch_url(url)

		if not response:
			return None

		if type(response) == bytes:
			response = response.decode("utf-8")

		stations = json.loads(response)
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

		response = fetch_url(url)

		if not response:
			return None

		if type(response) == bytes:
			response = response.decode("utf-8")

		result = json.loads(response)

		if session['configurations']['BVGLine']:
			line = session['configurations']['BVGLine'].lower()
			for _ in result:
				line_name = _['line']['name'].lower()
				if line in line_name:
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
		else:
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
