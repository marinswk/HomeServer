from flask import Flask, render_template, session, request, jsonify
import Database.HomeServerDBOperations as HomeServerDBOperations
from Database.HomeServerDBConnection import Configuration
import jsonpickle
import BvgApiCalls
import WeatherApiCalls
import GKeepApi

app = Flask(__name__)

configurations = HomeServerDBOperations.read_configurations()
config_dictionary = {x.name: x.value for x in configurations}

app.secret_key = config_dictionary["FlaskSecretKey"]


@app.route('/departures/<station_name>', methods=["GET"])
def get_current_departures_by_station_name(station_name):
	try:
		station = BvgApiCalls.get_station_id_by_name(station_name)
		if station:
			departures = BvgApiCalls.get_station_departures(station.id)
			return jsonpickle.encode(departures)
		else:
			return render_template('Errors.html')

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/display/<station_name>', methods=["GET"])
@app.route('/display', defaults={'station_name': None}, methods=["GET"])
def get_display_page(station_name):
	try:
		if station_name:
			return render_template('Display.html', station_name=station_name)
		else:
			return render_template('StationSelector.html')

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/weather/<city_name>/<country>', methods=["GET"])
def get_city_weather(city_name, country):
	try:
		city = WeatherApiCalls.get_city(city_name, country)
		if city:
			weather = WeatherApiCalls.get_city_weather_by_id(city['id'])
			return jsonpickle.encode(weather)

		else:
			return render_template('Errors.html')

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/weather/display/<city_name>/<country>', methods=["GET"])
def display_city_weather(city_name, country):
	try:
		if city_name and country:
			return render_template('Weather.html', city_name=city_name, country=country)
		else:
			return render_template('StationSelector.html')

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/gkeep/getgrocerieslist', methods=["GET"])
def get_groceries_list():
	try:

		response = GKeepApi.get_keep_groceries_list()
		if response["Status"]:
			return jsonpickle.encode(response["Items"])
		else:
			return render_template('Errors.html', error_message=response["Exception"])

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/home', methods=["GET"])
def display_home():
	try:
		session['configurations'] = config_dictionary
		return render_template(
			'Home.html',
			station_name=config_dictionary["BVGStationName"],
			city_name=config_dictionary["WeatherCityName"],
			country=config_dictionary["WeatherCountry"]
		)

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/', methods=["GET"])
def display_settings_page():
	try:

		if config_dictionary:
			return render_template('Configurations.html', config=config_dictionary)

	except Exception as ex:

		return render_template('Errors.html', error_message=str(ex))


@app.route('/writeconfigurations', methods=["POST"])
def write_configurations():
	try:
		data = request.json
		global configurations
		global config_dictionary

		for key, value in data.items():
			HomeServerDBOperations.write_configuration(Configuration(
				name=key,
				value=value
			))

		configurations = HomeServerDBOperations.read_configurations()
		config_dictionary = {x.name: x.value for x in configurations}
		session['configurations'] = config_dictionary

		return jsonify(Status=True)

	except Exception as ex:

		print(ex)
		return jsonify(Status=False)


if __name__ == '__main__':
	app.run()
