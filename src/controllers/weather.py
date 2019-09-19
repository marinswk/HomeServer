from flask import Blueprint, render_template
import jsonpickle
from src.modules import WeatherApiCalls

weather_endpoints = Blueprint('weather_endpoints', __name__, template_folder='templates')


@weather_endpoints.route('/weather/<city_name>/<country>', methods=["GET"])
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


@weather_endpoints.route('/weather/display/<city_name>/<country>', methods=["GET"])
def display_city_weather(city_name, country):
    try:
        if city_name and country:
            return render_template('Weather.html', city_name=city_name, country=country)
        else:
            return render_template('StationSelector.html')

    except Exception as ex:

        return render_template('Errors.html', error_message=str(ex))
