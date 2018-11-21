import pyowm
from influxdb import InfluxDBClient
import time
import sys


def getWeatherDetailsAtCords(owm, lat, lng):
    observation = owm.weather_at_coords(lat, lng)
    return observation.get_weather()

def sendDictToInflux(dict, client):
    if dict:
        json_body = [
            {
                "measurement": "open_weather_data",
                "tags": {
                    "location": "home"
                },
                "fields": {}
            }
        ]

        for key, value in dict.iteritems():
            json_body[0]['fields'][key] = value

        client.write_points(json_body)

def sendToInflux(dataName, value, client):
     if value is not None:
        json_body = [
            {
                "measurement": "open_weather_data",
                "tags": {
                    "location": "home"
                },
                "fields": {
                    dataName: value
                }
            }
        ]


        client.write_points(json_body)

def main(argv):
    owm = pyowm.OWM('76b37d4118ddc94a41b2344a4b2dc84a') #openWeatherApiKey
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'weather_data')

    while True:
        w = getWeatherDetailsAtCords(owm, 48.016686, 13.487734)

        sendDictToInflux(w.get_wind(), client)
        sendDictToInflux(w.get_temperature('celsius'), client)
        sendDictToInflux(w.get_rain(), client)
        sendDictToInflux(w.get_snow(), client)
        sendDictToInflux(w.get_pressure(), client)
        
        sendToInflux('hum', w.get_humidity(), client)
        sendToInflux('clouds', w.get_clouds(), client)
        sendToInflux('heat_index', w.get_heat_index(), client)
        sendToInflux('visible_distance', w.get_visibility_distance(), client)
    
        time.sleep(60)


if __name__ == "__main__":
    main(sys.argv)



