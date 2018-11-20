import pyowm
from influxdb import InfluxDBClient
import time
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

def sendRainData(rain_1h, rain_3h, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "rain"
            },
            "fields": {
                "rain_1h": rain_1h,
                "rain_3h": rain_3h
            }
        }
    ]

    client.write_points(json_body)

def sendSnowData(snow_1h, snow_3h, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "snow"
            },
            "fields": {
                "snow_1h": snow_1h,
                "snow_3h": snow_3h
            }
        }
    ]

    client.write_points(json_body)

def sendCloudData(coverage, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "cloud_coverage"
            },
            "fields": {
                "coverage": coverage
            }
        }
    ]

    client.write_points(json_body)

def sendHeatIndexData(heat_index, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "heat_index"
            },
            "fields": {
                "heat_index": heat_index
            }
        }
    ]

    client.write_points(json_body)

def sendPreasureData(preasure, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "preasure"
            },
            "fields": {
                "preasure": preasure
            }
        }
    ]

    client.write_points(json_body)

def sendVisibleDistanceData(visibleDistance, client):
    json_body = [
        {
            "measurement": "open_weather_data",
            "tags": {
                "location": "home",
                "type": "visible_distance"
            },
            "fields": {
                "visibleDistance": visibleDistance
            }
        }
    ]

    client.write_points(json_body)


def main(argv):
    owm = pyowm.OWM('76b37d4118ddc94a41b2344a4b2dc84a') #openWeatherApiKey
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'weather_data')

    while True:
        w = getWeatherDetailsAtCords(owm, 48.016686, 13.487734)
        print(w.get_wind())

        if 'speed' in w.get_wind() and 'deg' in w.get_wind():
            sendWindData(w.get_wind()['speed'], w.get_wind()['deg'], client)
        
        sendHumidityData(w.get_humidity(), client)
        sendTemperatureData(w.get_temperature('celsius')['temp'], w.get_temperature('celsius')['temp_max'], w.get_temperature('celsius')['temp_min'], client)
        sendRainData(w.get_rain()['1h'], w.get_rain()['3h'], client)
        sendSnowData(w.get_snow()['1h'], w.get_snow()['3h'], client)
        sendCloudData(w.get_clouds(),client)
        sendHeatIndexData(w.get_heat_index(),client)
        sendPreasureData(w.get_pressure()['press'], client)
        sendVisibleDistanceData(w.get_visibility_distance(), client)
        time.sleep(60)


if __name__ == "__main__":
    main(sys.argv)



