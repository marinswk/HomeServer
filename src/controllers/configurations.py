from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from src.modules import db_operations, Support
from src.models.configuration import Configuration

config_endpoints = Blueprint('config_endpoints', __name__, template_folder='templates')


@config_endpoints.route('/configure', methods=["GET"])
def display_settings_page():
    try:
        config_dictionary = Support.get_config_dictionary()
        return render_template('Configurations.html', config=config_dictionary)

    except Exception as ex:

        return render_template('Errors.html', error_message=str(ex))


@config_endpoints.route('/writeconfigurations', methods=["POST"])
def write_configurations():
    try:
        data = request.json

        for key, value in data.items():
            db_operations.write_configuration(Configuration(
                name=key,
                value=value
            ))

        return redirect(url_for('index'))

    except Exception as ex:

        print(ex)
        return jsonify(Status=False)
