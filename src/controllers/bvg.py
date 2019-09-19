from flask import Blueprint, render_template
import jsonpickle
from src.modules import BvgApiCalls

bvg_endpoints = Blueprint('bvg_endpoints', __name__, template_folder='templates')


@bvg_endpoints.route('/departures/<station_name>', methods=["GET"])
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


@bvg_endpoints.route('/display/<station_name>', methods=["GET"])
@bvg_endpoints.route('/display', defaults={'station_name': None}, methods=["GET"])
def get_display_page(station_name):
    try:
        if station_name:
            return render_template('Display.html', station_name=station_name)
        else:
            return render_template('StationSelector.html')

    except Exception as ex:

        return render_template('Errors.html', error_message=str(ex))
