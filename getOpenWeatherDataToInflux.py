import pyowm
from influxdb import InfluxDBClient
import time
import sys

def createInfluxRequestFromDict(dict):
    json_body = {}
    if dict:
        json_body = {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home"
            },
            "fields": {}
        }

        for key, value in dict.iteritems():
            if value is not None:
                json_body['fields'][key] = value

    return json_body

def createInfluxRequest(dataName, value):
    json_body = {}
    if value is not None:
        json_body = {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home"
            },
            "fields": {}
        }

        if isInstance(value, int) or isInstance(value, float):
            json_body['fields'] = float(value)
        else:
            json_body['fields'] = value
    return json_body

def main(argv):
    owm = pyowm.OWM('76b37d4118ddc94a41b2344a4b2dc84a') #openWeatherApiKey
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'weather_data')

    while True:
        time.sleep(120)

        #get the weather data from openweathermap
        w = owm.weather_at_coords(48.016686, 13.487734).get_weather()
        uv = owm.uvindex_around_coords(48.016686, 13.487734)

        requests = []

        requests.append(createInfluxRequestFromDict(w.get_wind()))
        requests.append(createInfluxRequestFromDict(w.get_temperature('celsius')))
        requests.append(createInfluxRequestFromDict(w.get_rain()))
        requests.append(createInfluxRequestFromDict(w.get_snow()))
        requests.append(createInfluxRequestFromDict(w.get_pressure()))
        
        requests.append(createInfluxRequest('hum', w.get_humidity()))
        requests.append(createInfluxRequest('clouds', w.get_clouds()))
        requests.append(createInfluxRequest('heat_index', w.get_heat_index()))
        requests.append(createInfluxRequest('visible_distance', w.get_visibility_distance()))
        requests.append(createInfluxRequest('uv_index', uv.get_value()))

        #remove the empty requests
        requests = filter(None, requests)

        #send to influxdb
        client.write_points(requests)
    

if __name__ == "__main__":
    main(sys.argv)



