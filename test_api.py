import json
import pandas
from main import app
from unittest import TestCase
from fastapi.testclient import TestClient




class TestSensorApi(TestCase):

    def setUp(self):
        with TestClient(app) as client:
            self.client = client
        good_file = pandas.read_csv("sensor.csv")
        self.g_file = pandas.DataFrame(good_file)

    def test_get_data(self):
        response = self.client.get("/get_data")
        self.assertEqual(response.status_code, 200)

    def test_parser_data(self):
        data = {
            "sensor_07": [
        {
            "timestamp": "2018-04-19T09:09:00.000",
            "machine_status": "RECOVERING",
            "medición": 21.12992
        }],
            "sensor_47": [{
            "timestamp": "2018-04-19T09:09:00.000",
            "machine_status": "RECOVERING",
            "medición": 21.12992
            }]
        }
        expected_data = [
        {
            "fecha": "2018-04-19T00:00:00.000Z",
            "hora": "09:09:00",
            "sensor": "07",
            "medición": 21.12992,
            "estado": "RECOVERING"
        },
        {
            "fecha": "2018-04-19T00:00:00.000Z",
            "hora": "09:09:00",
            "sensor": "47",
            "medición": 21.12992,
            "estado": "RECOVERING"
        }
    ]
        response = self.client.post("/parser_data", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], expected_data)