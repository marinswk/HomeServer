from flask import Blueprint, render_template
import jsonpickle
from src.modules import GKeepApi

gkeep_endpoints = Blueprint('gkeep_endpoints', __name__, template_folder='templates')


@gkeep_endpoints.route('/gkeep/getgrocerieslist', methods=["GET"])
def get_groceries_list():
    try:

        response = GKeepApi.get_keep_groceries_list()
        if response["Status"]:
            return jsonpickle.encode(response["Items"])
        else:
            return render_template('Errors.html', error_message=response["Exception"])

    except Exception as ex:

        return render_template('Errors.html', error_message=str(ex))
