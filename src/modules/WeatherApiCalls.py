from src.modules.Support import fetch_url, convert_utc_unix_timestamp_to_local_time_string, compare_dates, \
	get_config_dictionary
import json


weather_image_base_url = 'http://openweathermap.org/img/w/'  # attach image id and .png at the end of the string


class Weather:

	def __init__(self, weather_dict):

		self.name = weather_dict['name']
		self.main = weather_dict['weather'][0]['main']
		self.description = weather_dict['weather'][0]['description']
		self.icon_id = weather_dict['weather'][0]['id']
		self.icon_url = 'http://openweathermap.org/img/w/' + weather_dict['weather'][0]['icon'] + '.png'
		self.temp = weather_dict['main']['temp']
		self.pressure = weather_dict['main']['pressure']
		self.humidity = weather_dict['main']['humidity']
		self.temp_min = weather_dict['main']['temp_min']
		self.temp_max = weather_dict['main']['temp_max']
		self.wind_speed = weather_dict['wind']['speed']
		self.sunrise = convert_utc_unix_timestamp_to_local_time_string(weather_dict['sys']['sunrise'])
		self.sunset = convert_utc_unix_timestamp_to_local_time_string(weather_dict['sys']['sunset'])

		if compare_dates(weather_dict['sys']['sunrise'], weather_dict['sys']['sunset']):
			self.icon_suffix = '-d'
		else:
			self.icon_suffix = '-n'


def get_city_weather_by_id(city_id):
	try:
		config = get_config_dictionary()
		url = "https://api.openweathermap.org/data/2.5/weather?id=" + str(city_id) \
			+ "&units=metric&appid=" + config['OpenWeatherMapApiKey']

		response = fetch_url(url)
		if type(response) == bytes:
			response = response.decode("utf-8")
		weather_dict = json.loads(response)
		weather_object = Weather(weather_dict)

		return weather_object

	except Exception as ex:

		print(ex)
		raise ex


def __load_cities():
	try:
		with open('Data/city.list.json', encoding="utf8") as json_data:
			cities = json.load(json_data)
			return cities

	except Exception as ex:

		print(ex)
		raise ex


def get_city(name, country):
	try:
		cities = __load_cities()

		for city in cities:
			if name.lower() in city['name'].lower():
				if country.lower() in city['country'].lower():
					return city

	except Exception as ex:

		print(ex)
		raise ex
