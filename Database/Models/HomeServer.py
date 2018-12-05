class Configuration:

	def __init__(self, name, value, description, conf_id=None):
		self.id = conf_id
		self.name = name
		self.value = value
		self.description = description

