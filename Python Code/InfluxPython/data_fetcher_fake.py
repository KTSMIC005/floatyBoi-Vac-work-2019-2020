def get_recent_data():
    json_body = [
        {
            "measurement": "sensorEvents",
            "tags": {
                "sensor_name": "floaty_boi_001",
                "sensorId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
            },
            "time": "2018-03-28T8:01:00Z",
            "fields": {
                "air_temperature": -4.0,
                "wind_speed": 10.0,
                "wind_direction" : 270, #degreees
                "position": "68°01'12.0\"S 32°33'56.3\"E",
                "humidity": 90.5,
                "pressure": 1024
            }
        },
        {
            "measurement": "sensorEvents",
            "tags": {
                "sensor_name": "floaty_boi_001",
                "sensorId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
            },
            "time": "2018-03-28T8:01:00Z",
            "fields": {
                "air_temperature": -4.4,
                "wind_speed": 10.3,
                "wind_direction" : 273, #degreees
                "position": "68°01'12.0\"S 32°33'56.3\"E",
                "humidity": 91.5,
                "pressure": 1023
            }
        }
    ]



    return json_body