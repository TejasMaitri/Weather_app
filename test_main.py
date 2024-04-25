import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO
import main

class TestWeatherApp(unittest.TestCase):

    @patch('main.requests.get')
    def test_fetch_weather_details_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Goa",
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 28, "feels_like": 30, "pressure": 1010, "humidity": 60},
            "visibility": 10000,
            "wind": {"speed": 3.1, "deg": 270}
        }
        mock_get.return_value = mock_response

        expected_weather_details = {
            "City": "Goa",
            "Weather": {"Condition": "Clear", "Description": "clear sky"},
            "Main": {"Temperature": 28, "Feels Like": 30, "Pressure": 1010, "Humidity": 60},
            "Visibility": 10000,
            "Wind": {"Speed": 3.1, "Direction": 270}
        }

        actual_weather_details = main.fetch_weather_details("Goa")
        self.assertEqual(actual_weather_details, expected_weather_details)

    @patch('main.requests.get')
    def test_fetch_weather_details_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        actual_weather_details = main.fetch_weather_details("InvalidCity")
        self.assertIsNone(actual_weather_details)

    # Add more test cases for other functions as needed

if __name__ == "__main__":
    unittest.main()
