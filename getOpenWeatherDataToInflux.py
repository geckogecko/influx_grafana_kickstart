import pyowm
from influxdb import InfluxDBClient

import sys


def getWeatherDetailsAtCords(owm, lat, lng):
    observation = owm.weather_at_coords(lat, lng)
    return observation.get_weather()


def sendWindData(windSpeed, windDeg, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "wind"
            },
            "fields": {
                "speed": windSpeed,
                "deg": windDeg
            }
        }
    ]

    client.write_points(json_body)

def sendHumidityData(humidity, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "humidity"
            },
            "fields": {
                "humidity": humidity
            }
        }
    ]

    client.write_points(json_body)

def sendTemperatureData(temp, temp_max, temp_min, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "temperature"
            },
            "fields": {
                "temp": temp,
                "temp_max": temp_max,
                "temp_min": temp_min
            }
        }
    ]

    client.write_points(json_body)


def main(argv):
    owm = pyowm.OWM('76b37d4118ddc94a41b2344a4b2dc84a') #openWeatherApiKey
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'weather_data')

    while(True):
        w = getWeatherDetailsAtCords(owm, 48.016686, 13.487734)
        sendWindData(w.get_wind()['speed'], w.get_wind()['deg'], client)
        sendHumidityData(w.get_humidity(), client)
        sendTemperatureData(w.get_temperature('celsius')['temp'], w.get_temperature('celsius')['temp_max'], w.get_temperature('celsius')['temp_min'])

if __name__ == "__main__":
    main(sys.argv)



