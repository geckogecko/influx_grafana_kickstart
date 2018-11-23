from influxdb import InfluxDBClient
import time
import sys
import Adafruit_DHT


def createInfluxRequestFromDict(dict):
    json_body = {}
    if dict:
        json_body = {
            "measurement": "temp_data",
            "tags": {
                "location": "office"
            },
            "fields": {}
        }

        for key, value in dict.iteritems():
            if value is not None:
                json_body['fields'][key] = manipulateValue(value)

    return json_body

def createInfluxRequest(dataName, value):
    json_body = {}
    if value is not None:
        json_body = {
            "measurement": "temp_data",
            "tags": {
                "location": "office"
            },
            "fields": {
                dataName: manipulateValue(value)
            }
        }
    return json_body

#int -> float
#float -> float
#string -> string
def manipulateValue(value):
    if isinstance(value, int) or isinstance(value, float):
        return float(value)
    return value

def main(argv):
	sensor = Adafruit_DHT.DHT11
	pin = 4
	client = InfluxDBClient('93.90.200.187', 8086, 'root', 'root', 'temp_data')

	while True:
		try:
			time.sleep(300)
			#get the data from dht22
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
			
			#send to influxdb
			requests = []

			requests.append(createInfluxRequest('hum', humidity))
			requests.append(createInfluxRequest('temp', temperature))
			client.write_points(requests)
		except Exception as e:
			print(str(e))
    

if __name__ == "__main__":
    main(sys.argv)

