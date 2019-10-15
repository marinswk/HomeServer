import asyncio
from ourgroceries import OurGroceries
from src.modules.Support import get_config_dictionary


def get_groceries_list():
    try:
        config = get_config_dictionary()
        username = config['OurGroceriesUsername']
        password = config['OurGroceriesPassword']
        groceries_list_name = config['OurGroceriesListName']
        list_id = None
        list_items = None

        og = OurGroceries(username, password)
        asyncio.run(og.login())

        my_lists = asyncio.run(og.get_my_lists())

        for list in my_lists['shoppingLists']:
            if list['name'] == groceries_list_name:
                list_id = list['id']

        if list_id:
            list_items = asyncio.run(og.get_list_items(list_id))

        if list_items:
            items = list_items['list']['items']
            items[:] = [d for d in items if d.get('crossedOff') != True]
            return items
        else:
            return False

    except Exception as ex:

        print(ex)
        raise ex
