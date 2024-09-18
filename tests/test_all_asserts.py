import unittest
from unittest.mock import patch
import requests #Permite hacer solicitudes HTTP


def division(a,b):
    if b == 0:
        raise ZeroDivisionError("La divisón por cero no esta permitida")
    else:
        return a/b
    
class AllAssertsTests(unittest.TestCase):

    def test_assert_equal(self):
        self.assertEqual(10, 10)
        self.assertEqual("Hola", "Hola")


    def test_assert_true_or_false(self):
        self.assertTrue(True)
        self.assertFalse(False)


    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            int("no_soy_un_numero")


    def test_assert_in(self):
        self.assertIn(10, [2, 4, 5, 10])
        self.assertNotIn(5, [2, 4, 10])


    def test_assert_dicts(self):
        user = {
            "first_name": "Luis", 
            "last_name": "Martinez"
		}
        
        self.assertDictEqual(
            {
            "first_name": "Luis", 
            "last_name": "Martinez"
            },
            user
        )
        self.assertSetEqual(
            {1, 2, 3},
            {1, 2, 3}
        )
        
        
    def test_division_by_zero(self):
        #Falla a menos que reciba la excepción correcta como parámetro, si recibe otro tipo de exeption fallará
        with self.assertRaises(ZeroDivisionError): 
            division(10, 0) 

    @unittest.skip("Trabjo en progreso, será habilitada nuevamente")
    def test_skip(self):
        self.assertEqual("hola", "chao")

    SERVER="server_b"
    @unittest.skipIf(SERVER == "server_b", "Ignorado porque no estamos en el servidor")
    def test_skip_if(self):
        self.assertEqual(100, 100)

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.assertEqual(100, 150)
    
    
    # Con la siguiente función se verifica si la API está dispoible:
    def is_api_available(api):
        url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/oportuno?token={api}'
        response = requests.get(url)
        return response.status_code == 200
    # Se agrega conversión a USD, condicionada a disponibilidad de API
    # Se utiliza skipUnless en caso de que la API no esté disponible.
    @unittest.skipUnless(is_api_available('e3980208bf01ec653aba9aee3c2d6f70f6ae8b066d2545e379b9e0ef92e9de25'), 'API no disponible')
    @patch('src.bank_account.get_exchange_rate')
    def test_convert_to_usd(self, mock_get_exchange_rate):
        mock_get_exchange_rate.return_value = 20  # Ejemplo de tipo de cambio
        usd_balance = self.account.convert_to_usd(self.api)
        assert usd_balance == 50  # 1000/20 = 50