from src.modules import Support, WeatherApiCalls, BvgApiCalls


class HomeHelper:

    def __init__(self):
        self.config_dictionary = Support.get_config_dictionary()
        self.city_name = self.config_dictionary["WeatherCityName"]
        self.country = self.config_dictionary["WeatherCountry"]
        self.station_name = self.config_dictionary["BVGStationName"]

    def get_weather_data(self):
        try:
            city = WeatherApiCalls.get_city(self.city_name, self.country)
            if city:
                weather = WeatherApiCalls.get_city_weather_by_id(city['id'])
                return weather
            else:
                return False
        except Exception as e:
            print(e)
            raise e

    def get_bvg_data(self):
        try:
            station = BvgApiCalls.get_station_id_by_name(self.station_name)
            if station:
                departures = BvgApiCalls.get_station_departures(station.id)
                return departures
            else:
                return False
        except Exception as e:
            print(e)
            raise e
