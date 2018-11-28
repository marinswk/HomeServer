from flask import Flask, jsonify, render_template
import jsonpickle
import ApiCalls

app = Flask(__name__)


@app.route('/departures/<station_name>', methods=["GET"])
def get_current_departures_by_station_name(station_name):
	try:
		station = ApiCalls.get_station_id_by_name(station_name)
		if station:
			departures = ApiCalls.get_station_departures(station.id)
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


if __name__ == '__main__':
	app.run()