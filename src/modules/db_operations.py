from src.models.configuration import Configuration
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


def read_configurations():
	try:

		config = Configuration.query.all()
		return config

	except Exception as ex:

		print(ex)
		raise ex
