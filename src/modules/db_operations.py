from src.models.configuration import Configuration
from src.models.cryptocurrencies import CryptoWalletConfig, CryptoWalletManualAssets, ETHBlockchainAddresses
from app import db


def write_configuration(configuration):
	try:

		existing_config = Configuration.query.filter(Configuration.name == configuration.name).first()

		if existing_config:
			Configuration.query.filter(
				Configuration.name == configuration.name).update(
				dict(
					value=configuration.value
				))
		else:
			config =\
				Configuration(
					name=configuration.name,
					value=configuration.value
				)

			db.session.add(config)

		db.session.commit()

	except Exception as ex:

		print(ex)
		raise ex


def read_configurations(is_crypto=False):
	try:
		if is_crypto:
			config = CryptoWalletConfig.query.all()
		else:
			config = Configuration.query.all()
		return config

	except Exception as ex:

		print(ex)
		raise ex


def get_crypto_wallet_config_by_key(key):
	try:
		return CryptoWalletConfig.query.filter(CryptoWalletConfig.name == key).first().value

	except Exception as ex:

		print(ex)
		raise ex


def get_manual_assets():
	try:
		return CryptoWalletManualAssets.query.all()

	except Exception as ex:

		print(ex)
		raise ex


def get_eth_addresses():
	try:
		return ETHBlockchainAddresses.query.all()

	except Exception as ex:

		print(ex)
		raise ex
