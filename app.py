from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='homeserver', template_mode='bootstrap3')


from src.controllers.bvg import bvg_endpoints
from src.controllers.weather import weather_endpoints
from src.controllers.gkeep import gkeep_endpoints
from src.controllers.cryptocurrencies import crypto_endpoints
from src.controllers.home import home_endpoints
from src.models.configuration import Configuration
from src.models.cryptocurrencies import CryptoWalletConfig, CryptoWalletManualAssets, ETHBlockchainAddresses

admin.add_view(ModelView(Configuration, db.session))
admin.add_view(ModelView(CryptoWalletConfig, db.session))
admin.add_view(ModelView(CryptoWalletManualAssets, db.session))
admin.add_view(ModelView(ETHBlockchainAddresses, db.session))

app.register_blueprint(bvg_endpoints)
app.register_blueprint(weather_endpoints)
app.register_blueprint(gkeep_endpoints)
app.register_blueprint(crypto_endpoints)
app.register_blueprint(home_endpoints)

app.secret_key = Config.SECRET_KEY

if __name__ == '__main__':
    app.run()
