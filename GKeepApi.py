from flask import session
import gkeepapi


def get_keep_groceries_list():
	try:
		username = session['configurations']['GKeepUsername']
		psw = session['configurations']['GKeepPassword']
		groceries_list_id = session['configurations']['GKeepGroceriesId']

		keep = gkeepapi.Keep()
		success = keep.login(username, psw)

		if success:

			groceries = keep.get(groceries_list_id)
			groceries_items = groceries.unchecked

			groceries_list = []

			for _ in groceries_items:
				groceries_list.append(_.text)

			return {
				"Status": True,
				"Items": groceries_list
			}
		else:
			return {
				"Status": False,
				"Exception": str(success)
			}

	except Exception as ex:

		print(ex)
		return {
			"Status": False,
			"Exception": str(ex)
		}
