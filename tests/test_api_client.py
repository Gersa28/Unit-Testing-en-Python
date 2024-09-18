import unittest

import requests  # Importa el framework de pruebas unitarias de Python
from src.api_client import get_location  # Importa la función que será probada
from unittest.mock import patch  # Importa patch para hacer mocking de funciones

class ApiClientTests(unittest.TestCase):  # Define una clase de prueba que hereda de unittest.TestCase


    @patch('src.api_client.requests.get')  # Hace un mock del método requests.get en el módulo api_client, nos crea la variable mock_get que pasamos como parámetro
    def test_get_location_returns_expected_data(self, mock_get):  # Define una prueba que recibe mock_get
        # Configura el mock para que devuelva un status_code de 200
        mock_get.return_value.status_code = 200
        # Configura el mock para que devuelva un JSON con los datos de localización esperados
        mock_get.return_value.json.return_value = { # Imitamos la respuesta REAL después de inspeccinar data en api_client.py
            "countryName": "USA",
            "regionName": "FLORIDA",
            "cityName": "MIAMI",
        }
        # Llama a la función get_location pasando la IP "8.8.8.8"
        result = get_location("8.8.8.8")
        # Verifica que el país en el resultado sea "USA"
        self.assertEqual(result.get("country"), "USA")
        # Verifica que la región en el resultado sea "FLORIDA"
        self.assertEqual(result.get("region"), "FLORIDA")
        # Verifica que la ciudad en el resultado sea "MIAMI"
        self.assertEqual(result.get("city"), "MIAMI")

        # Asegura que requests.get fue llamado exactamente una vez con la URL correcta
        mock_get.assert_called_once_with("https://freeipapi.com/api/json/8.8.8.8")
    
        
    # Utiliza side_effect para simular diferentes respuestas en las llamadas a una API, 
    # incluyendo un fallo inicial y una respuesta exitosa después
    @patch("src.api_client.requests.get")  # Mockea el método requests.get en el módulo src.api_client
    def test_get_location_returns_side_effect(self, mock_get):  # Define la prueba unitaria que recibe el mock como parámetro
        # Configura el mock para tener dos efectos consecutivos:
        # 1. La primera llamada lanzará una excepción simulando un error de servicio no disponible.
        # 2. La segunda llamada devolverá un objeto Mock con un código de estado 200 y una respuesta JSON simulada.
        mock_get.side_effect = [ # side effect es una lista
            requests.exceptions.RequestException("Service Unavailable"),  # Simula un error en la primera llamada
            unittest.mock.Mock(  # Simula una respuesta exitosa en la segunda llamada
                status_code = 200,  # El código de estado HTTP será 200 (éxito)
                json = lambda: {  # La respuesta simulada será un JSON con los datos de geolocalización
                    "countryName": "USA",
                    "regionName": "FLORIDA",
                    "cityName": "MIAMI",
                },
            ),
        ]

        # 1º: Verifica que la primera llamada a get_location lanza la excepción RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            get_location("8.8.8.99")

        # 2º: La segunda llamada a get_location será exitosa y devolverá la respuesta JSON simulada
        result = get_location("8.8.8.8")
        
        # Verifica que el país devuelto sea "USA"
        self.assertEqual(result.get("country"), "USA")
        
        # Verifica que la región devuelta sea "FLORIDA"
        self.assertEqual(result.get("region"), "FLORIDA")
        
        # Verifica que la ciudad devuelta sea "MIAMI"
        self.assertEqual(result.get("city"), "MIAMI")

# python -m unittest tests.test_api_client.ApiClientTests.test_get_location_returns_side_effect -v
