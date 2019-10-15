from flask import Blueprint, render_template
from src.modules import home

home_endpoints = Blueprint('home_endpoints', __name__, template_folder='templates')


@home_endpoints.route('/', methods=['GET'])
def index():
    try:
        home_helper = home.HomeHelper()
        weather_data = home_helper.get_weather_data()
        bvg_data = home_helper.get_bvg_data()
        return render_template('index.html', weather_data=weather_data, bvg_data=bvg_data,
                               station_name=home_helper.station_name)
    except Exception as e:
        print(e)
