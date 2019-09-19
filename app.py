from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from src.controllers.bvg import bvg_endpoints
from src.controllers.weather import weather_endpoints
from src.controllers.gkeep import gkeep_endpoints
from src.controllers.configurations import config_endpoints
from src.models.configuration import Configuration
from src.modules import Support

app.register_blueprint(bvg_endpoints)
app.register_blueprint(weather_endpoints)
app.register_blueprint(gkeep_endpoints)
app.register_blueprint(config_endpoints)

app.secret_key = Config.SECRET_KEY


@app.route('/', methods=["GET"])
def index():
    try:
        config_dictionary = Support.get_config_dictionary()
        if config_dictionary:
            return render_template(
                'Home.html',
                station_name=config_dictionary["BVGStationName"],
                city_name=config_dictionary["WeatherCityName"],
                country=config_dictionary["WeatherCountry"]
            )
        else:
            return render_template('Configurations.html')

    except Exception as ex:

        return render_template('Errors.html', error_message=str(ex))


if __name__ == '__main__':
    app.run()
