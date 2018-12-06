from Database.HomeServerDBConnection import session, Configuration


def write_configuration(configuration):
	try:
		session.expire_all()

		existing_config = session.query(Configuration).filter(Configuration.name == configuration.name).first()

		if existing_config:
			session.query(Configuration).filter(
				Configuration.name == configuration.name).update(
				dict(
					value=configuration.value
				))
		else:
			session.merge(
				Configuration(
					name=configuration.name,
					value=configuration.value
				)
			)

		session.commit()
		session.close()

	except Exception as ex:

		print(ex)
		session.rollback()
		session.close()
		raise ex


def read_configurations():
	try:

		session.expire_all()
		config = session.query(Configuration).all()
		session.close()
		return config

	except Exception as ex:

		print(ex)
		session.close()
		raise ex
